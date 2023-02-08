from aiogram import *
import sqlite3
import asyncio
from messges import *
from union import BotDB
from aiogram.utils.markdown import hlink
from aiogram import types
import aiogram.utils.exceptions

conn = sqlite3.connect('orders.db')
cur = conn.cursor()
API_TOKEN = ''

PAYMENT_TOKEN = '381764678:TEST:38798'
admins = [915073363, 1058211493, 1800315908]
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
BotDB = BotDB('chatId.db')

loop = asyncio.new_event_loop()
if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
    # executor.start_polling(dp, loop=loop)
