import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import BOT_TOKEN, TELEGRAM_PROXY
from sql import create_pool,create_db

# loop = asyncio.get_event_loop()

storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML", proxy=TELEGRAM_PROXY)
dp = Dispatcher(bot, storage=storage)

db = dp.loop.run_until_complete(create_pool())
