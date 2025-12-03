import sqlite3
from typing import Any
from .config import DB_PATH


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            full_name TEXT,
            date TEXT NOT NULL,              -- YYYY-MM-DD
            messages_count INTEGER NOT NULL
        );
        """
    )

    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_activity_chat_date ON user_activity(chat_id, date);"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_activity_chat_user_date ON user_activity(chat_id, user_id, date);"
    )

    conn.commit()
    conn.close()
