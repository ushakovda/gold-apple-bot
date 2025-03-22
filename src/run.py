import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
import logging
from handlers import main_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logging.getLogger("aiogram").setLevel(logging.WARNING)
dp.include_router(main_router)


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
