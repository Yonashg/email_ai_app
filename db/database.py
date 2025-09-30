# db/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "emails.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            category TEXT,
            summary TEXT,
            reply TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_email(content, category, summary, reply):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO emails (content, category, summary, reply) VALUES (?, ?, ?, ?)",
        (content, category, summary, reply)
    )
    conn.commit()
    conn.close()

def fetch_emails():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, content, category, summary, reply FROM emails ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
