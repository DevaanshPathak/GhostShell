import argparse
import json
import os
from datetime import datetime
from ghostshell.sniffer import get_connections
from ghostshell.log_db import init_db, insert_connections
from rich import print
from ghostshell.detector import detect_suspicious, load_rules

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_log_path():
    date_str = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"ghostshell_{date_str}.jsonl")

def log_to_db(debug=False, write_json=False, rules=None):
    init_db()
    conns = get_connections()

    if rules:
        conns = detect_suspicious(conns, rules)

    insert_connections(conns)

    if write_json:
        with open("logs/snapshot.json", "w", encoding="utf-8") as f:
            json.dump(conns, f, indent=2)

    if debug:
        for conn in conns:
            print(f"[bold cyan][{conn.get('time', 'N/A')}][/bold cyan] "
                  f"[bold yellow]{conn.get('proto', 'N/A')}[/bold yellow] "
                  f"{conn.get('local', 'N/A')} → {conn.get('remote', 'N/A')} "
                  f"([green]{conn.get('status', 'N/A')}[/green], PID: {conn.get('pid', 'N/A')}, "
                  f"[magenta]{conn.get('country', 'N/A')}[/magenta], [blue]{conn.get('isp', 'N/A')}[/blue])")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GhostShell Logger")
    parser.add_argument("--debug", action="store_true", help="Print log output to terminal")
    parser.add_argument("--json", action="store_true", help="Also write logs to .json file")
    parser.add_argument("--rules", help="Path to custom rules JSON", default=None)
    args = parser.parse_args()

    rules = None
    if args.rules:
        with open(args.rules, "r", encoding="utf-8") as f:
            rules = json.load(f)

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Logging snapshot...")
    log_to_db(debug=args.debug, write_json=args.json, rules=rules)
    print("✅ [green]Log snapshot written to logs/logs.db[/green]")
