from collections import Counter
import os
import json
from ipaddress import ip_address, IPv4Network

DEFAULT_RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.json")


def is_private_ip(ip: str) -> bool:
    try:
        return ip_address(ip).is_private
    except ValueError:
        return False

def extract_ip_port(addr: str):
    """Returns (ip, port) tuple from 'IP:PORT' string."""
    try:
        ip, port = addr.split(":")
        return ip, int(port)
    except (ValueError, AttributeError):
        return None, None
    
def load_rules(path=DEFAULT_RULES_PATH):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load rules: {e}")
        return {}
#xyz test
def detect_suspicious(connections, rules):
    suspicious_entries = []

    max_conn_per_ip = rules.get("max_connections_per_ip", 100)
    malicious_countries = set(rules.get("malicious_countries", []))
    max_conn_per_local_port = rules.get("max_connections_per_local_port", 20)
    suspicious_private_ports = set(rules.get("suspicious_private_ports", []))

    # Count connections per remote IP
    remote_ips = [extract_ip_port(conn.get("remote", ""))[0] for conn in connections if conn.get("remote")]
    remote_ip_counts = Counter(ip for ip in remote_ips if ip)

    # Count connections per local port
    local_ports = []
    for conn in connections:
        _, local_port = extract_ip_port(conn.get("local", ""))
        if local_port is not None:
            local_ports.append(local_port)
    local_port_counts = Counter(local_ports)

    # RFC1918 private IP ranges
    private_networks = [
        IPv4Network("10.0.0.0/8"),
        IPv4Network("172.16.0.0/12"),
        IPv4Network("192.168.0.0/16")
    ]

    for conn in connections:
        reasons = []

        remote_str = conn.get("remote", "")
        local_str = conn.get("local", "")
        country = conn.get("country", "")

        remote_ip, remote_port = extract_ip_port(remote_str)
        _, local_port = extract_ip_port(local_str)

        # Rule 1: Too many connections to one IP
        if remote_ip and remote_ip_counts[remote_ip] > max_conn_per_ip:
            reasons.append(f"High number of connections to {remote_ip}")

        # Rule 2: Malicious country
        if country in malicious_countries:
            reasons.append(f"Connection to malicious country ({country})")

        # Rule 3: Too many connections from same local port
        if local_port is not None and local_port_counts[local_port] > max_conn_per_local_port:
            reasons.append(f"Excessive use of local port {local_port}")

        # Rule 4: Private IP with suspicious local port
        try:
            if remote_ip and ip_address(remote_ip) in [net for net in private_networks]:
                if local_port in suspicious_private_ports:
                    reasons.append(f"Suspicious private IP {remote_ip} with local port {local_port}")
        except ValueError:
            pass  # skip malformed IPs

        if reasons:
            suspicious_entries.append({**conn, "suspicious": True, "reason": "; ".join(reasons)})
        else:
            suspicious_entries.append({**conn, "suspicious": False, "reason": ""})

    return suspicious_entries
