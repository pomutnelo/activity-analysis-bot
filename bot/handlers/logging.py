from aiogram import Router, F
from aiogram.types import Message

from ..services.activity_service import add_message_activity

router = Router()


@router.message(F.chat.type.in_(["group", "supergroup"]))
async def log_group_messages(message: Message):
    
    if message.from_user is None or message.from_user.is_bot:
        return

    user = message.from_user
    username = user.username
    full_name = (user.full_name or "").strip()

    add_message_activity(
        chat_id=message.chat.id,
        user_id=user.id,
        username=username,
        full_name=full_name,
    )
