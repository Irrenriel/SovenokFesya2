from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient
from aiogram import Bot, Dispatcher
import asyncio

from bin.config import *
from bot.classes.settings_class import Scheduler_ex, SQLite_db, Middleware


# Loop
loop = asyncio.get_event_loop()

# Scheduler
scheduler = Scheduler_ex(loop)

# MemoryStorage
storage = MemoryStorage()

# Bot
bot = Bot(token=BOT_TOKEN, loop=loop, parse_mode=PARSE_MODE)

# Client Sessions
main_client = TelegramClient(MAIN_SESSION_NAME, API_ID, API_HASH, loop=loop)
brief_client = TelegramClient(BRIEF_SESSION_NAME, API_ID, API_HASH, loop=loop)

# Dispatcher
dp = Dispatcher(bot, storage=storage, loop=loop)

# Database
db = SQLite_db(db='bin/{}.db'.format(DB_NAME))
dp.middleware.setup(Middleware(db))