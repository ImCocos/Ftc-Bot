import os
import random
import pip
pip.main(['install', 'pytelegrambotapi'])
import sqlite3
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from Data import data
from AliveKeeper import keep_alive


start_balance = data['START_BALANCE']
ImCocosKingId = data['CREATOR_ID']
API_TOKEN = data['API_TOKEN']
c = 0
# Initializing bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Create user's data base
def create_users_bd():
    con = sqlite3.connect('users.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id BIGINT, name TEXT, premium BOOLEAN, balance BIGINT)')
    con.commit()

# SQLite3 connection
con = sqlite3.connect('users.db')
cur = con.cursor()


# Auth and Start
@dp.message_handler(commands = ['start'])
async def start(message: types.Message):

    # SQLite3 connection
    con = sqlite3.connect('users.db')
    cur = con.cursor()

    # User existion
    user_exists = False
    check_user_existance(message)

    # Get user's data
    user_unique_id = message.from_user.id
    user_name = message.from_user.first_name
    user_have_premium = bool(message.from_user.is_premium)
    user_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{user_unique_id}"').fetchone()[0]


    if user_unique_id != ImCocosKingId:
        await message.reply(f"Привет, {user_name}!\n"
                            f"Это твой профиль:\n"
                            f"  Имя: {user_name}\n"
                            f"  Премиум: {user_have_premium}\n"
                            f"  Баланс: {user_balance} FTC\n")
    else:
        await message.reply(f"Приветствую,\n"
                            f"мой Король {user_name}!\n"
                            f"Это твой профиль:\n"
                            f"  Имя: {user_name}\n"
                            f"  Премиум: {user_have_premium}\n"
                            f"  Баланс: {user_balance} FTC\n")


@dp.message_handler(lambda message: ('б' == message.text.lower()) or ('баланс' == message.text.lower()))
async def balance_show(message: types.Message):
    # Important func
    check_user_existance(message)
    # SQLite3 connection
    con = sqlite3.connect('users.db')
    cur = con.cursor()

    # Get user's data
    user_unique_id = message.from_user.id
    user_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{user_unique_id}"').fetchone()[0]
    await message.reply(f"Баланс: {user_balance}")


@dp.message_handler(lambda message: (message.text[0] == '+'))
async def transfer(message: types.Message):
    # Important func
    check_user_existance(message)

    try:
        transaction_value = int(message.text)

        if message.reply_to_message['from']['is_bot'] == False:

            # SQLite3 connection
            con = sqlite3.connect('users.db')
            cur = con.cursor()

            sender_name = message.from_user.first_name
            getter_name = message.reply_to_message['from']['first_name']
            sender_unique_id = message.from_user.id
            sender_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{sender_unique_id}"').fetchone()[0]
            getter_unique_id = message.reply_to_message['from']['id']
            getter_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{getter_unique_id}"').fetchone()[0]

            if sender_balance >= transaction_value:
                cur.execute(f'UPDATE users SET balance = "{sender_balance - transaction_value}" WHERE id = "{sender_unique_id}"')
                cur.execute(f'UPDATE users SET balance = "{getter_balance + transaction_value}" WHERE id = "{getter_unique_id}"')
                con.commit()
                await bot.send_message(message.chat.id, f'{sender_name} перевел {transaction_value} {getter_name}.')
            else:
                await bot.send_message(message.chat.id, "Недостаточно FTC для перевода.")
        else:
            await message.reply("Ты не можешь перевести FTC боту!")

    except Exception:
        await message.reply(f"Запрос на перевод некорректный!")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    # Important func
    check_user_existance(message)
    await message.reply(f"На данный момент,\n"
                        f"бот имеет команды:\n"
                        f"  /start - старт бота и авторизация пользователя,\n"
                        f"  /help - список всех команд,\n"
                        f"  Баланс/Б - вывод текущего баланса,\n"
                        f"В ближайшие дни будут добавлены Бандит и Префиксы к имени!")

# Check user existance function(should be called in most of funcs)
def check_user_existance(message: types.Message):

    # SQLite3 connection
    con = sqlite3.connect('users.db')
    cur = con.cursor()

    # User existion
    user_exists = False

    # Get user's data
    user_unique_id = message.from_user.id
    user_name = message.from_user.first_name
    user_have_premium = bool(message.from_user.is_premium)

    # User existing check
    for user in cur.execute('SELECT * FROM users'):
        if user_unique_id != user[0]:
            user_exists = False
        else:
            user_exists = True
            user_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{user_unique_id}"').fetchone()[0]
            break
    if not user_exists:
        user_balance = start_balance
        cur.execute(f'INSERT INTO users VALUES("{user_unique_id}", "{user_name}", "{user_have_premium}", "{user_balance}")')
        con.commit()


def main():
    create_users_bd()
    keep_alive()
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
