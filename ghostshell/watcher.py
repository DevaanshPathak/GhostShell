import time
import argparse
from ghostshell.sniffer import get_connections
from ghostshell.detector import detect_suspicious
from ghostshell.geo import enrich_connections
from ghostshell.log_db import insert_connections
from ghostshell.rules import load_rules

WATCH_INTERVAL = 5  # seconds

def watch_mode(debug=False):
    rules = load_rules()

    print("[GhostShell] Watching for connections... (Press Ctrl+C to stop)")
    try:
        while True:
            conns = get_connections()
            enriched = enrich_connections(conns)
            flagged = detect_suspicious(enriched, rules)
            insert_connections(flagged)

            if debug:
                for conn in flagged:
                    print(f"[{conn['time']}] {conn['local']} -> {conn['remote']} | Suspicious: {conn['suspicious']} | Reason: {conn['reason']}")

            time.sleep(WATCH_INTERVAL)

    except KeyboardInterrupt:
        print("\n[GhostShell] Live monitoring stopped.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GhostShell Live Watcher")
    parser.add_argument('--debug', action='store_true', help='Print debug info to console')
    args = parser.parse_args()

    watch_mode(debug=args.debug)
