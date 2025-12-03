from datetime import datetime, timedelta
from typing import List

from ..db import get_db_connection


def add_message_activity(
    chat_id: int,
    user_id: int,
    username: str | None,
    full_name: str | None,
) -> None:
    
    today = datetime.utcnow().date().isoformat()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, messages_count
        FROM user_activity
        WHERE chat_id = ? AND user_id = ? AND date = ?
        """,
        (chat_id, user_id, today),
    )
    row = cur.fetchone()

    if row:
        new_count = row["messages_count"] + 1
        cur.execute(
            """
            UPDATE user_activity
            SET messages_count = ?, username = ?, full_name = ?
            WHERE id = ?
            """,
            (new_count, username, full_name, row["id"]),
        )
    else:
        cur.execute(
            """
            INSERT INTO user_activity (chat_id, user_id, username, full_name, date, messages_count)
            VALUES (?, ?, ?, ?, ?, 1)
            """,
            (chat_id, user_id, username, full_name, today),
        )

    conn.commit()
    conn.close()


def get_top_activity(chat_id: int, days: int = 1, limit: int = 10):
    
    conn = get_db_connection()
    cur = conn.cursor()

    from_date = (datetime.utcnow().date() - timedelta(days=days - 1)).isoformat()

    cur.execute(
        """
        SELECT user_id,
               COALESCE(username, '') AS username,
               COALESCE(full_name, '') AS full_name,
               SUM(messages_count) AS total_messages
        FROM user_activity
        WHERE chat_id = ?
          AND date >= ?
        GROUP BY user_id, username, full_name
        ORDER BY total_messages DESC
        LIMIT ?
        """,
        (chat_id, from_date, limit),
    )

    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_activity(chat_id: int, user_id: int, days: int = 7) -> int:
    
    conn = get_db_connection()
    cur = conn.cursor()

    from_date = (datetime.utcnow().date() - timedelta(days=days - 1)).isoformat()

    cur.execute(
        """
        SELECT SUM(messages_count) AS total_messages
        FROM user_activity
        WHERE chat_id = ?
          AND user_id = ?
          AND date >= ?
        """,
        (chat_id, user_id, from_date),
    )
    row = cur.fetchone()
    conn.close()

    if row and row["total_messages"]:
        return int(row["total_messages"])
    return 0
