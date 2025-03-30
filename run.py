import asyncio
from aiogram import Bot, Dispatcher, types
from src.config import TOKEN
import logging
from src.handlers import main_router
from db.db import init_db
from aiogram.fsm.storage.memory import MemoryStorage
from src.price_checker import check_prices_loop

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logging.getLogger("aiogram").setLevel(logging.WARNING)
dp.include_router(main_router)


async def on_startup():
    await init_db()

async def main():
    print("Бот запущен...")
    await on_startup()
    asyncio.create_task(check_prices_loop(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
