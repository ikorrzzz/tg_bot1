import asyncio
from aiogram import Bot, Dispatcher
from handlers_manager import router
import logging
import os

TOKEN = os.getenv("TOKEN")


async def main():
    logging.basicConfig(level=logging.INFO)  # Логирование
    bot = Bot(TOKEN)  # Связывались с серверами тг с нашим токеном
    dp = Dispatcher()  # Ловит апдейты
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
