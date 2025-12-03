import sqlite3
import logging
from pathlib import Path

from .config import DB_PATH


def get_db_connection() -> sqlite3.Connection:
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

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
            date TEXT NOT NULL,
            messages_count INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    conn.commit()
    conn.close()
    logging.info("DB initialized")
