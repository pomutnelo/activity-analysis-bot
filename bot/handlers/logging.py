import sqlite3
import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..config import DB_PATH

router = Router()
logger = logging.getLogger(__name__)


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- /top: топ за всё время ----------

@router.message(Command("top"))
async def cmd_top(message: Message):
    """
    /top — топ активных за ВСЁ время в этом чате.
    """
    if message.chat.type not in ("group", "supergroup"):
        await message.answer("Эта команда работает только в групповых чатах.")
        return

    chat_id = message.chat.id
    logger.info("TOP: got /top in chat_id=%s", chat_id)

    conn = _get_conn()

    # На всякий случай создаём таблицу (та же схема, что использует логгер)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()

    cur = conn.cursor()

    # Смотрим, сколько всего записей по этому чату
    cur.execute(
        "SELECT COUNT(*) AS cnt FROM activity_messages WHERE chat_id = ?",
        (chat_id,),
    )
    total_for_chat = cur.fetchone()["cnt"]
    logger.info("TOP_DEBUG: chat_id=%s total_rows_for_chat=%s", chat_id, total_for_chat)

    # Считаем топ пользователей
    cur.execute(
        """
        SELECT
            user_id,
            MAX(username)  AS username,
            MAX(full_name) AS full_name,
            COUNT(*)       AS total_messages
        FROM activity_messages
        WHERE chat_id = ?
        GROUP BY user_id
        ORDER BY total_messages DESC
        LIMIT 10;
        """,
        (chat_id,),
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        await message.answer("Пока нет данных по активности в этом чате.")
        logger.info("TOP_DEBUG: no rows for chat_id=%s", chat_id)
        return

    lines = ["<b>Топ активных за всё время:</b>\n"]
    for i, row in enumerate(rows, start=1):
        row = dict(row)
        name = row["full_name"] or row["username"] or f"id:{row['user_id']}"
        lines.append(f"{i}. {name} — {row['total_messages']} сообщений")

    logger.info("TOP_DEBUG: chat_id=%s returned_rows=%s", chat_id, len(rows))

    await message.answer("\n".join(lines), parse_mode="HTML")


# ---------- логирование всех сообщений ----------

@router.message()
async def log_message(message: Message):
    """
    Логируем КАЖДОЕ сообщение в группе / супергруппе.
    """
    if message.chat.type not in ("group", "supergroup"):
        return

    user = message.from_user
    if not user or user.is_bot:
        return

    conn = _get_conn()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS activity_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    full_name = " ".join(filter(None, [user.first_name, user.last_name]))

    conn.execute(
        """
        INSERT INTO activity_messages (chat_id, user_id, username, full_name)
        VALUES (?, ?, ?, ?)
        """,
        (message.chat.id, user.id, user.username, full_name),
    )
    conn.commit()
    conn.close()

    logger.info(
        "LOG_MESSAGE: chat_type=%s, user_id=%s, text=%r",
        message.chat.type,
        user.id,
        message.text,
    )
