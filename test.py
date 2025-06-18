import json
from ghostshell.sniffer import get_connections
from ghostshell.detector import detect_suspicious

with open("./ghostshell/suspicious_rules.json") as f:
    rules = json.load(f)

connections = get_connections()
print(f"🔍 Got {len(connections)} connections")  # DEBUG

suspicious_connections = detect_suspicious(connections, rules)
print(f"⚠️ Found {sum(1 for c in suspicious_connections if c['suspicious'])} suspicious connections")  # DEBUG


for conn in suspicious_connections:
    if conn['suspicious']:
        print(f"{conn['time']} {conn['proto']} {conn['local']} → {conn['remote']} [SUSPICIOUS] Reason: {conn['reason']}")
