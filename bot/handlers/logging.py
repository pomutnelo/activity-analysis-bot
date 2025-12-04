import sqlite3
import logging
from aiogram import Router, F
from aiogram.types import Message
from ..config import DB_PATH

router = Router()
logger = logging.getLogger(__name__)

def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.message(F.content_type != "web_app_data")
async def log_message(message: Message):

    if message.chat.type not in ("group", "supergroup"):
        return

    user = message.from_user
    if not user:
        return

    logger.info(f"LOG_MESSAGE: user={user.id}, text={message.text}")

    conn = _get_conn()
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

    conn.execute(
        "INSERT INTO activity_messages (chat_id, user_id, username, full_name) VALUES (?, ?, ?, ?)",
        (message.chat.id, user.id, user.username, full_name),
    )

    conn.commit()
    conn.close()
