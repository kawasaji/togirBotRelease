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


def get_users_id():
    conn = sqlite3.connect("chatId.db")
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM `users`")
    a = users.fetchall()
    conn.commit()
    conn.close()
    return a

def get_chats_id():
    conn = sqlite3.connect("chatId.db")
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM `chats`")
    a = users.fetchall()
    conn.commit()
    conn.close()
    return a

@dp.chat_join_request_handler()
async def say_hello(message: types.Message):

    await bot.approve_chat_join_request(
                          message.chat.id,
                          message.from_user.id)
# async def join(update: types.ChatJoinRequest, message: types.Message):
#     await bot.send_message(message.chat.id, "hello")
#
# @dp.message_handler(content_types=types.content)
# async def say_hello(message: types.Message):
#     await bot.send_message(message.chat.id, "hello")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if not BotDB.user_exists(message.from_user.id):
            BotDB.add_user(message.from_user.id)
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if not BotDB.chat_exists(message.chat.id):
            BotDB.add_chat(message.chat.id)
    await message.reply("дарова")

@dp.message_handler(commands=['exit'])
async def start(message: types.Message):
    await message.reply("exit...")
    os.system("exit")

@dp.message_handler(commands=['buy'])
async def buy_process(message: types.Message):
    await bot.send_invoice(message.chat.id,
                           title="title",
                           description="description",
                           provider_token=PAYMENT_TOKEN,
                           currency='rub',
                           need_name=True,
                           is_flexible=True,
                           prices=PRICES,
                           start_parameter='example',
                           payload='some_invoice')

@dp.shipping_query_handler(lambda q: True)
async def shipping_process(shipping_query: ShippingQuery):
    if shipping_query.shipping_address.country_code == 'AZ':
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
        )

@dp.message_handler(commands=['go'])
async def buy_process(message: types.Message):
    await message.reply("ok")

@dp.message_handler(commands=['getUsers'])
async def getUsers(message: types.Message):
    if message.from_user.id in admins:
        users = get_users_id()
        await message.reply(f"Количество пользователей в базе данных: {len(users)}")
    else:
        await message.reply("Вы не админ бота.")
@dp.message_handler(commands=['getChats'])
async def getUsers(message: types.Message):
    if message.from_user.id in admins:
        chats = get_chats_id()
        await message.reply(f"Количество чатов в базе данных: {len(chats)}")
    else:
        await message.reply("Вы не админ бота.")

@dp.message_handler(commands=['sendAllChats'])
async def getUsers(message: types.Message):
    a = message.text.split()
    b = " ".join(a[1::])
    chats = get_chats_id()
    count = 0
    if message.from_user.id in admins:
        await message.answer("Начинаю...")
        for i in range(len(chats)):
            try:
                await bot.send_message(chats[i][1], text=b)
                count += 1
            except aiogram.utils.exceptions.BotBlocked:
                BotDB.delete_user(chats[i][0])
            except aiogram.utils.exceptions.BotKicked:
                BotDB.delete_user(chats[i][0])
            except aiogram.utils.exceptions.CantInitiateConversation:
                BotDB.delete_user(chats[i][0])
        await message.answer(f"Всё! Колличество отправленных сообщений: {count}")

    else:
        await message.answer("Вы не админ")

@dp.message_handler(commands=['sendAllUsers'])
async def getUsers(message: types.Message):
    a = message.text.split()
    b = " ".join(a[1::])
    users = get_users_id()
    count = 0
    if message.from_user.id in admins:
        await message.answer("Начинаю...")
        for i in range(len(users)):
            try:
                await bot.send_message(users[i][1], text=b)
                count += 1
            except aiogram.utils.exceptions.BotBlocked:
                BotDB.delete_user(users[i][0])
            except aiogram.utils.exceptions.BotKicked:
                BotDB.delete_user(users[i][0])
            except aiogram.utils.exceptions.CantInitiateConversation:
                BotDB.delete_user(users[i][0])

        await message.answer(f"Всё! Колличество отправленных сообщений: {count}")

    else:
        await message.answer("Вы не админ")


@dp.message_handler(commands=['get'])
async def getChatId(message: types.Message):
    await message.reply(message.chat.id)


@dp.message_handler(commands=['send'])
async def sendChatId(message: types.Message):
    if message.from_user.id in admins or message.from_user.user.id in admins:
        try:
            message_temp = message.text.split()
            a = " ".join(message_temp[2::])
            # await bot.send_message(chat_id=message_temp[1], text=a)
            await bot.send_message(chat_id=message_temp[1], text=a, parse_mode="Markdown")
            await message.reply("Сообщение отправлено.")
        except aiogram.utils.exceptions.BotBlocked:
            await message.reply("Пользователь заблокировал бота")
        except aiogram.utils.exceptions.CantInitiateConversation:
            await message.reply("Невозможно начать чат с пользователем.")
        except aiogram.utils.exceptions.ChatNotFound:
            await message.reply("Чат не найден.")
    else:
        await message.reply("Вы не админ.")


@dp.message_handler(content_types=['text'], text='dick')
async def record(message: types.Message):
    variants = [-10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "2X", "NULL"]
    value = random.choice(variants)
    print(value)
    # BotDB.add_record(message.from_user.id, value)
    if value == "2X":
        await message.reply(f'Ваш писюн увеличился в 2 раза!\nТеперь ваш писюн равен: см')
    elif value == "NUll":
        await message.reply(f'Ваш писюн обнулился!\nТеперь ваш писюн равен 0 см')
    elif 1 <= value <= 10:
        await message.reply(f'Ваш писюн увеличился на {value}см!\nТеперь ваш писюн равен: см')
    elif -10 <= value <= -1:
        await message.reply(f'Ваш писюн уменьшился на {value}см!\nТеперь ваш писюн равен: см')


@dp.message_handler(commands=['del'])
async def delMessage(message: types.Message):
    text = message.text.split()
    print(text)
    if message.from_user.id in admins:
        if len(text) == 1:
            if message.chat.type == 'private':
                await message.reply("Команда не работает в личных сообщениях с ботом")
            elif message.chat.type == 'supergroup' or message.chat.type == 'group':
                a = await bot.get_chat_administrators(chat_id=message.chat.id)
                a = str(a)
                b = str(message.from_user.id)
                c = str(message.from_user.username)
                if b in a or c in a:
                    try:
                        message_id = message.reply_to_message.message_id
                        message_user_id = message.message_id
                        await bot.delete_message(chat_id=message.chat.id, message_id=message_id)
                        await bot.delete_message(chat_id=message.chat.id, message_id=message_user_id)
                    except aiogram.utils.exceptions.MessageCantBeDeleted:
                        await message.reply("Бот не является админом в беседе")
                    except AttributeError:
                        await message.reply("Неправильный формат команды\n"
                                            "Ответьте на сообщение которое вы хотите удалить.")
                else:
                    await message.reply("Вы не являетесь админом в беседе.")
        else:
            await message.reply("Неправильный формат команды.")
    else:
        await message.reply("Вы не админ")


@dp.message_handler(commands=['snus'])
async def snus(message: types.Message):
    a = random.choice([0, 1])
    if a == 0:
        await message.reply("Ода! Вы попали прямо в рот!")
    else:
        await message.reply("Упс! Ваш снюс упал на пол!")


@dp.message_handler(commands=['call'])
async def callBot(message: types.Message):
    a = random.choice([0, 1])
    if a == 0:
        await message.reply("здраствуйте")
    else:
        await message.reply("досвидание")


@dp.message_handler(commands=['stop'])
async def notice(message: types.Message):
    if message.from_user.id in admins:
        a = message.text.split()
        b = "".join(a[2::])
        data_time = int(a[1])
        await message.reply(f"Бот остановлен на {data_time} минут")
        data_time *= 60
        timing = time.time()
        while True:
            if time.time() - timing > data_time:
                timing = time.time()
                await message.reply(b)
                break
    else:
        await message.reply("Вы не админ")


@dp.message_handler(commands=['replyTo'])
async def image(message: types.Message):
    if message.from_user.id in admins:
        try:
            a = message.text.split()
            print(a)
            b = " ".join(a[3::])
            await bot.send_message(chat_id=a[1], reply_to_message_id=a[2], text=b)
        except IndexError:
            await  message.reply("Неправильный формат сообщения")
        except aiogram.utils.exceptions.ChatNotFound:
            await message.reply("Чат не найден")
        except aiogram.utils.exceptions.BadRequest:
            await message.reply("Не найдено айди сообщения")

    # await bot.send_message(chat_id=message.chat.id, reply_to_message_id=a[1], text=b)


@dp.message_handler(commands=['meme'])
async def image(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    if not BotDB.user_exists(message.chat.id):
        BotDB.add_user(message.chat.id)
    a = message.text.split()
    if len(a) == 1:
        await message.reply("Неправильный формат команды.")
    else:
        b = " ".join(a[1::])
        temp = createImage(b)
        if temp:
            temp_image = open("jak_memes/last.jpg", 'rb')
            await bot.send_photo(chat_id=message.chat.id, photo=temp_image)
        if not temp:
            await message.reply("Длина сообщения превышает 100 символов!")


@dp.message_handler(commands=['kill'])
async def image(message: types.Message):
    a = [True, False]
    b = random.choice(a)
    if b:
        await message.reply("Лошпед, тебе не повезло")
        await bot.send_sticker(chat_id=message.chat.id,
                               sticker=r"CAACAgIAAxkBAAEE1QRikJtFxCMVbgdQIpCCJIMjcEZgdQACmBcAAlEHOUuu61__uvQ7NiQE")
        await bot.kick_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    else:
        await message.reply("Вам повезло, будьте осторожны в следющий раз!")
        await bot.send_sticker(chat_id=message.chat.id,
                               sticker=r"CAACAgIAAxkBAAEE4OVilQm9Qg27gXds8vs3kNMOnY4ujwAC-xkAAuOHWUvkPi9WizrQNyQE")


@dp.message_handler(commands=['len'])
async def lenOut(message: types.Message):
    b = message.text.split()

    a = " ".join(b[1::])
    c = "Длина сообщения равна: " + str(len(a)) + " символов"
    await message.reply(c)


@dp.message_handler(commands=['list'])
async def listOut(message: types.Message):
    a = "Ахмедлы группа - `-1001591824435`\nШкольная группа - `-1001216883171`\nШестой группа - `-1001497164843`"
    await bot.send_message(chat_id=message.chat.id, text=a, parse_mode="Markdown")



@dp.message_handler(commands=['help'])
async def helpOut(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    if not BotDB.user_exists(message.chat.id):
        BotDB.add_user(message.chat.id)
    await message.reply("Список команд:\n"
                        "/call - позвать бота\n"
                        "/snus - кинуть снюс\n"
                        "/kill - русская рулетка\n"
                        "/meme (текст) - сделать цитату\n"
                        "тянка - отправляет рандомную аниме тянку")


@dp.message_handler(commands=['admin'])
async def helpAdmin(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=admin_text, parse_mode="HTML")


@dp.message_handler(commands=['type'])
async def image(message: types.Message):
    if message.from_user.id in admins:
        message_id = message.reply_to_message.message_id
        chat_id = message.chat.id
        text = str("`/replyTo " + str(chat_id) + " " + str(message_id) + "`")
        await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode="Markdown")
    else:
        await message.reply("Вы не админ")


@dp.message_handler(commands=['getId'])
async def getId(message: types.Message):
    # b = message.text.split()
    text = message.reply_to_message.from_user.id
    await bot.send_message(chat_id=message.chat.id, text=text)


@dp.message_handler(commands=['getMessageId'])
async def getMessageId(message: types.Message):
    a = message.reply_to_message.message_id
    await message.reply(a)


@dp.message_handler(commands=['admins'])
async def getId(message: types.Message):
    print(await bot.get_chat_administrators(chat_id=message.chat.id))
    a = await bot.get_chat_administrators(chat_id=message.chat.id)

    # y = json.loads(a)
    a = str(a)
    if "kawasaji" in a:
        print("ok")
    listA = list(a)
    listA.pop(0)
    listA.pop(-1)
    a = "".join(listA)
    a = str(a)
    print(a)
    a = a.replace("{", "[")
    a = a.replace("}", "]")
    b = set(await bot.get_chat_administrators(chat_id=message.chat.id))
    print(a)
    print(b)
    await message.reply(await bot.get_chat_administrators(chat_id=message.chat.id))
    print(b[0][0][0])


@dp.message_handler(commands=['ok'])
async def kickUser(message: types.Message):
    BotDB.set_status(message.from_user.id, 1)
    await message.reply("ok")


@dp.message_handler(commands=['kick'])
async def kickUser(message: types.Message):
    if message.chat.type == "private":
        if not BotDB.user_exists(message.from_user.id):
            BotDB.add_user(message.from_user.id)
    elif message.chat.type == "group" or message.chat.type == "supergroup":
        if not BotDB.user_exists(message.chat.id):
            BotDB.add_chat(message.chat.id)
    if message.chat.type == 'private':
        await message.reply("Команда не работает в личных сообщениях с ботом")
    elif message.chat.type == 'supergroup' or message.chat.type == 'group':
        a = await bot.get_chat_administrators(chat_id=message.chat.id)
        a = str(a)
        b = str(message.from_user.id)
        c = str(message.from_user.username)
        if b in a or c in a:
            a = message.text.split()
            if len(a) == 1:
                try:
                    text = message.reply_to_message.from_user.id
                    text_temp = "Я выебал " + str(message.reply_to_message.from_user.first_name)
                    await bot.kick_chat_member(chat_id=message.chat.id, user_id=text)
                    await bot.send_message(chat_id=message.chat.id, text=text_temp)
                except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                    await message.reply("Пользователь является админом чата")
                except aiogram.utils.exceptions.BadRequest:
                    await message.reply("Неправильный ID пользователя\n"
                                        "Введите сообщение в формате например: /kick 1657303362\n"
                                        "Или в ответ на сообщения пользователя")

            elif len(a) == 2:
                try:
                    await bot.kick_chat_member(chat_id=message.chat.id, user_id=a[1])
                    await message.reply("ok")

                except aiogram.utils.exceptions.UserIsAnAdministratorOfTheChat:
                    await message.reply("Пользователь является админом чата")

                except aiogram.utils.exceptions.BadRequest:
                    await message.reply("Неправильный ID пользователя\n"
                                        "Введите сообщение в формате например: /kick 1657303362\n"
                                        "Или в ответ на сообщения пользователя")
            else:
                await message.reply("Неправильный формат команды")
        else:
            await message.reply("Команда ограничена.\n"
                                "Вы не админ.")


@dp.message_handler(content_types=['text'])
async def reply(message: types.Message):
    if message.chat.type == "private":
        if not BotDB.user_exists(message.from_user.id):
            BotDB.add_user(message.from_user.id)
    if message.chat.type == "group" or message.chat.type == "supergroup":
        if not BotDB.chat_exists(message.chat.id):
            BotDB.add_chat(message.chat.id)
    '''
    if message.from_user.id == 1826023868 or message.from_user.id == 1657303362 or message.from_user.id == 5236126147:
        answers = ['тебя забыть спросили', 'че ты пиздишь в моем районе', 'заткнись', 'смешно', 'завали',
                   'помолчи да, надоел уже', 'бля, опять он начал...', 'мама неджяди', 'мама неджяди',
                   'إلهي امنحني القوة', 'إلهي امنحني القوة']
        await message.reply(random.choice(answers))
    '''
    if "tiktok" in message.text.lower():
        await message.reply("тикток фигня")
    if "тоже" in message.text or "так" in message.text:
        await message.reply("да")
    if "ахуел" in message.text.lower():
        await message.reply("сам ахуел")
    if "+" in message.text.lower():
        await message.reply("+")
    if "привет" in message.text.lower():
        await message.reply("пока")
    if "соси" in message.text.lower():
        photo = open('files/test.jpg', 'rb')
        lol = message.from_user.first_name, "отсосал"
        await message.reply("сам соси, лошпед")
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        # await bot.send_message(chat_id=1058211493, text=lol)
    if "пизда" in message.text.lower():
        await message.reply("пошел нахуй")
    if "тянка" in message.text.lower():
        stickers_temp = [1, 2, 3, 4, 5, 6, 7, 8]
        a = random.choice(stickers_temp)
        if a == 1:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1P5ikJnYxAzwxLz75MO3YJNUrxoAAYEAAtAIAAJsO0Eo_92idGD7k5skBA")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1QABYpCamODbjL73zDbrKyl8rH1Sz2QAAtUIAAJsO0EoFHdOA6VnNqwkBA")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1QJikJrMCFNpGqkyDsHJdAooqani0wAC2ggAAmw7QShhib58AQdUhiQE")
        elif a == 2:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1hRikQihuA-hQ8u2TY5Ovbr3BcJJ8gAChggAAmw7QShsoXSEQ-70XyQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1hVikQiiWyi_rI9c2xk9gsGcmB46YAACiwgAAmw7QSiTLLqLOvekNyQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1hhikQim_OLh3dM4Kop_CC61-kUOkAACkAgAAmw7QSj6UUxciyQ4jiQE")
        elif a == 3:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1h5ikQjqz3r1il5CpF-xopiqP__w6wAChQgAAmw7QShyN_sF_NnHsyQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1iBikQjr-GBLAkmPr1e8Ahyf5Mk7PgACiggAAmw7QSjcU1CNpqvlXCQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEE1iJikQjvq5mSAyOzn0rlr5HJiu09rgACjwgAAmw7QSinM7gxksrebCQE")
        elif a == 4:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFEFirwpkYTEnqPAeuiAcCgaL45BfZwAChwgAAmw7QSjYYj_wwuNp0iQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFEJirwpmj-OnbXxwHnx0Rt_4DAgoMwACjAgAAmw7QShbbjPg5wwtoSQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFEVirwppSK4uJ0HM2Mm5oUetRLkWXgACkQgAAmw7QShfY2k4i9cQ1CQE")
        elif a == 5:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFEdirwqrys9u1ktODCFvCWX4fj5NdwAClwgAAmw7QSg5pyTVWtqdqiQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFElirwqsjfERizx0pPLpqzHDgP2BxQACnAgAAmw7QSjiZUtyPt9CkyQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFEtirwquJbqf5ZV3LRqNvTgd47e4BwACoQgAAmw7QSgeNLcULbsRfyQE")

        elif a == 6:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFE1irwrtGYfxp-fXr4qb4DH2TJUe4QAClggAAmw7QSjeluO7YVVuRiQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFE9irwruoV5ViKYc1MjuTn-bx6tTnAACmwgAAmw7QSh_AAEBR61Yb60kBA")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFFFirwrwNvlpe2sNsR3-7xkG1FpJegACoAgAAmw7QSgNqhEpbd12SiQE")

        elif a == 7:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFFNirws0gi4YfndsAimSVtWfAm5b6QACwwgAAmw7QShijuBDCkcVsiQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFFRirws2s3jdea-e1Kz_l6n0ZBIcMgACyAgAAmw7QSga2cflqjXThCQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFFdirws6GRO3p7uw1cQxScjGcWW86gACzggAAmw7QShQYbHL-C2YbCQE")
        elif a == 8:
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFFlirwtlENjpT5bS_Bi49ThSjbj7ngACsQgAAmw7QSi0_L1Bwy7nQSQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFFtirwtnb9rS4OV69JA3Gs6vmjfkMAACtggAAmw7QShwU86pxkIJ5SQE")
            await bot.send_sticker(chat_id=message.chat.id,
                                   sticker=r"CAACAgIAAxkBAAEFFF1irwtrvlnTU8Z4KPF6xlagLzQERwACuwgAAmw7QSjlDWAadDelCCQE")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
