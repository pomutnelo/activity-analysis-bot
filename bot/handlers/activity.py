from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from ..services.activity_service import get_top_activity, get_user_activity

router = Router()


@router.message(Command("activity_today"))
async def cmd_activity_today(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.answer("Эта команда работает только в групповых чатах.")
        return

    rows = get_top_activity(chat_id=message.chat.id, days=1, limit=10)
    if not rows:
        await message.answer("Сегодня нет зафиксированной активности.")
        return

    lines = ["Топ-10 активных за сегодня:"]
    for i, row in enumerate(rows, start=1):
        name = row["full_name"] or row["username"] or f"id:{row['user_id']}"
        lines.append(f"{i}. {name} — {row['total_messages']} сообщений")

    await message.answer("\n".join(lines))


@router.message(Command("activity_7d"))
async def cmd_activity_7d(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.answer("Эта команда работает только в групповых чатах.")
        return

    rows = get_top_activity(chat_id=message.chat.id, days=7, limit=10)
    if not rows:
        await message.answer("За последние 7 дней нет зафиксированной активности.")
        return

    lines = ["Топ-10 активных за 7 дней:"]
    for i, row in enumerate(rows, start=1):
        name = row["full_name"] or row["username"] or f"id:{row['user_id']}"
        lines.append(f"{i}. {name} — {row['total_messages']} сообщений")

    await message.answer("\n".join(lines))


@router.message(Command("my_activity"))
async def cmd_my_activity(message: Message):
    if message.chat.type not in ("group", "supergroup"):
        await message.answer("Эта команда работает только в групповых чатах.")
        return

    user = message.from_user
    if user is None:
        await message.answer("Не удалось определить пользователя.")
        return

    total_7d = get_user_activity(chat_id=message.chat.id, user_id=user.id, days=7)
    await message.answer(
        f"Ваша активность за последние 7 дней: {total_7d} сообщений."
    )
