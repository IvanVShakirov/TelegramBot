import asyncio
from aiogram import executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, TELEGRAM_PROXY, ADMIN_ID
from db_commands import DBCommands
from handlers import reg_handlers
from sql import create_pool, create_db


def main():
    storage = MemoryStorage()

    bot = Bot(token=BOT_TOKEN, parse_mode="HTML", proxy=TELEGRAM_PROXY)
    dp = Dispatcher(bot, storage=storage)
    pool = dp.loop.run_until_complete(create_pool())
    db = DBCommands(pool)

    async def on_shutdown(dp):
        await bot.close()

    async def on_startup(dp):
        await asyncio.sleep(10)
        await create_db()
        await bot.send_message(ADMIN_ID, "Я запущен!")

    reg_handlers(dp, bot, db)

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)


if __name__ == '__main__':
    main()
