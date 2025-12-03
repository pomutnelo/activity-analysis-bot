from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..services.activity_service import get_top_activity_all_time

router = Router()

@router.message(Command("top"))
async def cmd_top(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.answer("Эта команда работает только в группах.")
        return

    chat_id = message.chat.id
    rows = get_top_activity_all_time(chat_id=chat_id, limit=10)

    if not rows:
        await message.answer("Пока нет данных по активности в этом чате.")
        return

    lines = ["<b>Топ активности за всё время:</b>\n"]
    for i, row in enumerate(rows, start=1):
        name = (
            row["full_name"]
            or row["username"]
            or f"id:{row['user_id']}"
        )
        lines.append(f"{i}. {name} — {row['total_messages']} сообщений")

    await message.answer("\n".join(lines), parse_mode="HTML")
