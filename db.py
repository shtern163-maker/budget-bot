import sqlite3
from datetime import datetime

DB_NAME = "budget.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            amount INTEGER,
            is_income INTEGER,
            date TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS learning (
            word TEXT PRIMARY KEY,
            category TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_record(category, amount, is_income):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO records (category, amount, is_income, date) VALUES (?, ?, ?, ?)",
        (category, amount, int(is_income), datetime.now().strftime("%Y-%m-%d"))
    )

    conn.commit()
    conn.close()


def add_learning(word, category):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT OR REPLACE INTO learning (word, category) VALUES (?, ?)",
        (word, category)
    )

    conn.commit()
    conn.close()


def get_learned_category(text):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT word, category FROM learning")
    rows = c.fetchall()
    conn.close()

    for word, category in rows:
        if word in text:
            return category

    return None
