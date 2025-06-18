import requests
import ipaddress
import requests

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