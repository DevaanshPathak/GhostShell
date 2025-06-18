import sqlite3
import os

DB_PATH = os.path.join("logs", "logs.db")

def init_db():
    os.makedirs("logs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS connections (
            time TEXT,
            proto TEXT,
            local TEXT,
            remote TEXT,
            status TEXT,
            pid INTEGER,
            country TEXT,
            isp TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_connections(entries):
    import sqlite3
    conn = sqlite3.connect("logs/logs.db")
    c = conn.cursor()

    for entry in entries:
        entry.setdefault("country", "N/A")
        entry.setdefault("isp", "N/A")

    c.executemany("""
        INSERT INTO connections (time, proto, local, remote, status, pid, country, isp)
        VALUES (:time, :proto, :local, :remote, :status, :pid, :country, :isp)
    """, entries)

    conn.commit()
    conn.close()
