import sqlite3
from aiogram import Router
from aiogram.types import Message
import logging

from ..config import DB_PATH

router = Router()
logger = logging.getLogger(__name__)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.message()
async def log_message(message: Message):

    if not message.chat or message.chat.type not in ("group", "supergroup"):
        return

    if message.text and message.text.startswith("/top"):
        return  

    user = message.from_user
    if not user:
        return

    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    full_name = " ".join(filter(None, [user.first_name, user.last_name]))

    conn.execute("""
        INSERT INTO activity_messages (chat_id, user_id, username, full_name)
        VALUES (?, ?, ?, ?)
    """, (message.chat.id, user.id, user.username, full_name))

    conn.commit()
    conn.close()

    logger.info(f"Stored message in DB")
