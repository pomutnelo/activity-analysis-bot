import logging
from bot.db import get_connection  # ⚠️ только так
from bot.config import DB_PATH

logger = logging.getLogger(__name__)


def get_top_users(chat_id: int, limit: int = 10):
    """
    Возвращает список строк (sqlite3.Row):
    user_id, username, full_name, msg_count
    """
    logger.info(f"TOP REQUEST for chat={chat_id}, DB_PATH={DB_PATH}")

    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT user_id,
                   username,
                   full_name,
                   COUNT(*) AS msg_count
            FROM activity_messages
            WHERE chat_id = ?
            GROUP BY user_id
            ORDER BY msg_count DESC
            LIMIT ?
            """,
            (chat_id, limit),
        ).fetchall()
    finally:
        conn.close()

    logger.info(f"TOP rows fetched: {len(rows)}")
    return rows
