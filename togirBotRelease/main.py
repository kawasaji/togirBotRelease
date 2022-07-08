import aiogram.utils.exceptions
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery
from aiogram.types.message import ContentType
import random, time
from createImage import createImage
import sqlite3
import asyncio
from messges import *
import re
import os
from union import BotDB
from aiogram import types



PRICES = [
    LabeledPrice(label='Ноутбук', amount=1000),
    LabeledPrice(label='Прочная упаковка', amount=1000)
]

conn = sqlite3.connect('orders.db')
cur = conn.cursor()
API_TOKEN = '1888774189:AAEfUF-A8Lhp5GCetqkpZ7v5POrrA0j7ikE'
BOT_URL = 'https://togir-bot.herokuapp.com'
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

# if __name__ == '__main__':
#
