import argparse
import sqlite3
from rich.table import Table
from rich.console import Console

DB_PATH = "logs/logs.db"
console = Console()

def query_logs(ip=None, country=None, date=None, suspicious=False, limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    sql = "SELECT time, proto, local, remote, status, pid, country, isp, suspicious, reason FROM connections WHERE 1=1"
    params = []

    if ip:
        sql += " AND (local LIKE ? OR remote LIKE ?)"
        params += [f"%{ip}%", f"%{ip}%"]

    if country:
        sql += " AND country = ?"
        params.append(country.upper())

    if date:
        sql += " AND time LIKE ?"
        params.append(f"{date}%")  # assumes time is full timestamp if you switch later

    if suspicious:
        sql += " AND suspicious = 1"

    sql += " ORDER BY time DESC LIMIT ?"
    params.append(limit)

    c.execute(sql, tuple(params))
    rows = c.fetchall()
    conn.close()
    return rows

def display_table(rows):
    table = Table(title="GhostShell Log Viewer (SQLite)")

    table.add_column("Time", style="cyan", no_wrap=True)
    table.add_column("Proto", style="yellow")
    table.add_column("Local Address")
    table.add_column("Remote Address")
    table.add_column("Status", style="green")
    table.add_column("PID", style="bold")
    table.add_column("Country", style="magenta")
    table.add_column("ISP", style="blue")
    table.add_column("⚠️ Suspicious?", style="red")
    table.add_column("Reason", style="bold red")

    for row in rows:
        time, proto, local, remote, status, pid, country, isp, suspicious, reason = row
        is_suspicious = "[bold red]Yes[/bold red]" if suspicious else "No"
        table.add_row(time, proto, local, remote, status, str(pid), country, isp, is_suspicious, reason)

    console.print(table)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GhostShell Log Viewer (SQLite)")
    parser.add_argument("--ip", help="Search by IP or substring")
    parser.add_argument("--country", help="Filter by country code (e.g., IN)")
    parser.add_argument("--date", help="Filter by date (YYYY-MM-DD)")
    parser.add_argument("--suspicious", action="store_true", help="Show only suspicious entries")
    parser.add_argument("--limit", type=int, default=50, help="Limit results (default: 50)")

    args = parser.parse_args()
    logs = query_logs(
        ip=args.ip,
        country=args.country,
        date=args.date,
        suspicious=args.suspicious,
        limit=args.limit
    )

    if logs:
        display_table(logs)
    else:
        console.print("[red]No matching logs found.[/red]")
