import sqlite3
import json
from datetime import datetime, timezone
from src.models import MeetingSummary

DB_PATH = "meetings.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            created_at TEXT NOT NULL,
            transcript TEXT NOT NULL,
            summary_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_meeting(filename: str, transcript: str, summary: MeetingSummary) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "INSERT INTO meetings (filename, created_at, transcript, summary_json) VALUES (?, ?, ?, ?)",
        (filename, datetime.now(timezone.utc).isoformat(), transcript, summary.model_dump_json())
    )
    conn.commit()
    meeting_id = cursor.lastrowid
    conn.close()
    return meeting_id

def list_meetings():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT id, filename, created_at, summary_json FROM meetings ORDER BY id DESC").fetchall()
    conn.close()
    return rows
