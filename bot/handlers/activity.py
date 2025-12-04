import sqlite3
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..config import DB_PATH

router = Router()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@router.message(Command("top"))
async def cmd_top(message: Message):
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

    rows = conn.execute("""
        SELECT user_id, username, full_name, COUNT(*) AS msg_count
        FROM activity_messages
        WHERE chat_id = ?
        GROUP BY user_id
        ORDER BY msg_count DESC
        LIMIT 20
    """, (message.chat.id,)).fetchall()

    conn.close()

    if not rows:
        await message.answer("Пока нет данных по активности в этом чате.")
        return


    text = ["ТОП активных за всё время:", ""]
    for i, row in enumerate(rows, 1):
        username = f"@{row['username']}" if row["username"] else (row["full_name"] or "без имени")
        text.append(f"{i}. {username} — {row['msg_count']} сообщений")

  
    await message.answer("\n".join(text))

