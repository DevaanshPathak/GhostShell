import sqlite3

DB_PATH = "logs/logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            time TEXT,
            proto TEXT,
            local TEXT,
            remote TEXT,
            status TEXT,
            pid TEXT,
            country TEXT,
            isp TEXT,
            suspicious BOOLEAN DEFAULT 0,
            reason TEXT DEFAULT ''
        )
    """)
    conn.commit()
    conn.close()

def insert_connections(entries):
    # Sanitize each entry to ensure all required fields exist
    for entry in entries:
        entry.setdefault("time", "")
        entry.setdefault("proto", "")
        entry.setdefault("local", "")
        entry.setdefault("remote", "")
        entry.setdefault("status", "")
        entry.setdefault("pid", "")
        entry.setdefault("country", "N/A")
        entry.setdefault("isp", "N/A")
        entry.setdefault("suspicious", 0)
        entry.setdefault("reason", "")
        # Make sure suspicious is an int (SQLite expects 0/1)
        entry["suspicious"] = int(entry["suspicious"])

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executemany("""
        INSERT INTO connections (
            time, proto, local, remote, status, pid,
            country, isp, suspicious, reason
        ) VALUES (
            :time, :proto, :local, :remote, :status, :pid,
            :country, :isp, :suspicious, :reason
        )
    """, entries)
    conn.commit()
    conn.close()
