import argparse
import json
import os
from datetime import datetime
from ghostshell.sniffer import get_connections
from ghostshell.log_db import init_db, insert_connections
from rich import print
from ghostshell.detector import detect_suspicious

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_log_path():
    date_str = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"ghostshell_{date_str}.jsonl")

def log_to_db(debug=False, write_json=False):
    init_db()
    conns = get_connections()
    insert_connections(conns)

    if debug:
        for conn in conns:
            print(f"[bold cyan][{conn['time']}][/bold cyan] "
                  f"[bold yellow]{conn['proto']}[/bold yellow] "
                  f"{conn['local']} → {conn['remote']} "
                  f"([green]{conn['status']}[/green], PID: {conn['pid']}, "
                  f"[magenta]{conn['country']}[/magenta], [blue]{conn['isp']}[/blue])")

    if write_json:
        log_path = get_log_path()
        with open(log_path, "a", encoding="utf-8") as f:
            for conn in conns:
                json.dump(conn, f)
                f.write("\n")
        print(f"📄 [yellow]Log also written to {log_path}[/yellow]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GhostShell Logger")
    parser.add_argument("--debug", action="store_true", help="Print log output to terminal")
    parser.add_argument("--json", action="store_true", help="Also write logs to .jsonl file")
    args = parser.parse_args()

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Logging snapshot...")
    log_to_db(debug=args.debug, write_json=args.json)
    print("✅ [green]Log snapshot written to logs/logs.db[/green]")

conns = detect_suspicious(get_connections())