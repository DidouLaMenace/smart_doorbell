import sqlite3
from config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        with open("backend/database/schema.sql") as f:
            conn.executescript(f.read())

def log_event(event_type):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO events (event_type) VALUES (?)", (event_type,))
        conn.commit()

def get_all_events():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT * FROM events ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        return [{"id": r[0], "event_type": r[1], "timestamp": r[2]} for r in rows]
