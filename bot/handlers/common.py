from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, ChatMemberUpdated

router = Router()


@router.my_chat_member()
async def bot_added(update: ChatMemberUpdated, bot: Bot):
   
    if update.new_chat_member.user.id != bot.id:
        return

    if update.new_chat_member.status in ("member", "administrator"):
        await bot.send_message(
            update.chat.id,
              "Привет! Я бот для анализа активности участников в этом чате 👋\n\n"
    "Я считаю, сколько сообщений пишет каждый участник, чтобы можно было "
    "собирать статистику.\n\n"
            "Команда: /top — топ активных за всё время.",
        )


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start — на всякий случай, если кто-то запустит бота командой.
    """
    await message.answer(
          "Привет! Я бот для анализа активности участников в этом чате 👋\n\n"
    "Я считаю, сколько сообщений пишет каждый участник, чтобы можно было "
    "собирать статистику.\n\n"
        "Команда: /top — топ активных за всё время."
    )
