import sqlite3
from datetime import datetime

conn = sqlite3.connect("budget.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records (
    id INTEGER PRIMARY KEY,
    amount REAL,
    category TEXT,
    type TEXT,
    created_at TEXT
)
""")
conn.commit()


def add_record(amount, category, rtype):
    cursor.execute(
        "INSERT INTO records (amount, category, type, created_at) VALUES (?, ?, ?, ?)",
        (amount, category, rtype, datetime.now().isoformat())
    )
    conn.commit()


def get_month_stats():
    cursor.execute("""
    SELECT category, SUM(amount)
    FROM records
    WHERE type='expense'
      AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
    GROUP BY category
    """)
    return cursor.fetchall()


def get_month_total():
    cursor.execute("""
    SELECT type, SUM(amount)
    FROM records
    WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
    GROUP BY type
    """)
    return cursor.fetchall()
