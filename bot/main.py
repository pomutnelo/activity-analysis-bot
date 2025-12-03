import asyncio
import logging

from aiogram import Bot, Dispatcher

from .config import BOT_TOKEN
from .db import init_db
from .handlers import get_routers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        raise RuntimeError("Укажи токен бота в config.py или через переменную окружения BOT_TOKEN.")

    init_db()
    logging.info("DB initialized")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    for router in get_routers():
        dp.include_router(router)

    logging.info("Starting bot polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
