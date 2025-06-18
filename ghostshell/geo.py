import requests
import ipaddress
from ghostshell.utils import extract_ip, is_private_ip

def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def get_geo(ip):
    if ip.startswith("127.") or is_private_ip(ip):
        return {
            "country": "Local Network",
            "city": "-",
            "lat": 0,
            "lon": 0,
            "org": "-",
            "as": "-",
            "isp": "Local"
        }

    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = response.json()
        if data["status"] == "success":
            return {
                "country": data.get("country", "?"),
                "city": data.get("city", "?"),
                "lat": data.get("lat", 0),
                "lon": data.get("lon", 0),
                "org": data.get("org", "?"),
                "as": data.get("as", "?"),
                "isp": data.get("isp", "?")
            }
    except Exception:
        pass

    return {
        "country": "?",
        "city": "?",
        "lat": 0,
        "lon": 0,
        "org": "?",
        "as": "?",
        "isp": "?"
    }

def get_ip_location(ip: str):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        return data.get("country", "Unknown"), data.get("isp", "Unknown")
    except Exception:
        return "Unknown", "Unknown"
    
def enrich_connections(conns):
    """Mock geo enrichment for now — add country/ISP fields."""
    for conn in conns:
        remote_ip = extract_ip(conn["remote"])

        if not remote_ip or is_private_ip(remote_ip):
            conn["country"] = "N/A"
            conn["isp"] = "N/A"
        else:
            # Replace this block with real geolocation later
            conn["country"] = "RU" if remote_ip.startswith("8.") else "IN"
            conn["isp"] = "BadISP" if remote_ip.startswith("8.") else "GoodISP"

    return conns