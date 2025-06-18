from ghostshell.sniffer import get_connections #self made library (a/ghostshell/sniffer.py)

conns = get_connections()
for conn in conns:
    print(f"[{conn['timestamp']}] {conn['protocol']} {conn['local_address']} → {conn['remote_address']} "
          f"({conn['status']}, PID {conn['pid']})")
