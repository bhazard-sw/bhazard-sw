import sqlite3
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path("reports.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS agent_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            json_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_report(report_json: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    c.execute(
        "INSERT INTO agent_reports (timestamp, json_data) VALUES (?, ?)",
        (timestamp, json.dumps(report_json))
    )
    report_id = c.lastrowid
    conn.commit()
    conn.close()
    return report_id
