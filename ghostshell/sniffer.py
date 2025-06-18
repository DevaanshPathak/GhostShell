# ghostshell/sniffer.py

import psutil
import socket
from datetime import datetime
from ghostshell.geo import get_ip_location

def get_connections():
    conns = psutil.net_connections(kind='inet')
    results = []

    for conn in conns:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr_ip = conn.raddr.ip if conn.raddr else None
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        pid = conn.pid or "N/A"
        status = conn.status
        proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"

        # Geolocation lookup
        location = get_ip_location(raddr_ip) if raddr_ip else {"country": "", "region": "", "city": ""}

        results.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "proto": proto,
            "local": laddr,
            "remote": raddr,
            "status": status,
            "pid": pid,
            "location": location
        })

    return results
