import sqlite3
from pathlib import Path

DB_PATH = Path("portfolio.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    with open("persistence/schema.sql") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
