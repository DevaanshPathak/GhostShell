# ghostshell/utils.py

import ipaddress

def is_private_ip(ip: str) -> bool:
    """Check if an IP address is private (RFC1918 for IPv4, ULA for IPv6)."""
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def extract_ip(address: str) -> str:
    """Extract IP part from 'IP:Port' or return IP if already clean."""
    if not address or ':' not in address:
        return address
    # Handles both IPv4 and IPv6
    try:
        if address.count(':') > 1:  # IPv6
            if address.startswith('['):  # [IPv6]:Port
                return address.split(']')[0].lstrip('[')
            else:
                return address.rsplit(':', 1)[0]
        return address.split(':')[0]  # IPv4
    except Exception:
        return address

def extract_port(addr):
    if ":" in addr and not addr.startswith("["):
        return int(addr.rsplit(":", 1)[-1])
    if addr.startswith("[") and "]:" in addr:
        return int(addr.split("]:")[-1])
    return None


def safe_get(d: dict, key: str, default="N/A") -> str:
    """Safely get a value from a dict with a default."""
    return d.get(key, default)

