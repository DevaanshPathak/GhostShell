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
