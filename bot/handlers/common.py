from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ChatMemberUpdated
from aiogram.exceptions import TelegramForbiddenError

router = Router()

WELCOME_TEXT = (
    "Привет! Я бот для анализа активности участников в этом чате 👋\n\n"
    "Я считаю, сколько сообщений пишет каждый участник, чтобы можно было "
    "собирать статистику.\n\n"
    "Доступные команды:\n"
    "• /activity_today — топ-10 самых активных за сегодня\n"
    "• /activity_7d — топ-10 за последние 7 дней\n"
    "• /my_activity — ваша активность за 7 дней\n\n"
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/activity_today — топ за сегодня\n"
        "/activity_7d — топ за 7 дней\n"
        "/my_activity — ваша активность\n"
    )


@router.my_chat_member()
async def on_bot_added_to_chat(event: ChatMemberUpdated, bot: Bot):
    old = event.old_chat_member.status
    new = event.new_chat_member.status

    if old in ("left", "kicked") and new in ("member", "administrator"):
        try:
            await bot.send_message(event.chat.id, WELCOME_TEXT)
        except TelegramForbiddenError:
            return
