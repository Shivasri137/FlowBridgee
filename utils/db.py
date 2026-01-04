import sqlite3
import os
from datetime import datetime

DB_PATH = "data/professional_tasks.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def add_task(task_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (task_name, status, created_at)
        VALUES (?, ?, ?)
    """, (task_name, "Pending", datetime.now().isoformat()))

    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = ?, completed_at = ?
        WHERE id = ?
    """, ("Completed", datetime.now().isoformat(), task_id))

    conn.commit()
    conn.close()

def fetch_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()
    return rows
