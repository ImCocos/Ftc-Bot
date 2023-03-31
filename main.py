import os
import random
import time

import pip
pip.main(['install', 'aiogram'])
import sqlite3
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from Data import data
from AliveKeeper import keep_alive


start_balance = data['START_BALANCE']
ImCocosKingId = data['CREATOR_ID']
API_TOKEN = os.environ['API_TOKEN']
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
                await bot.send_message(message.chat.id, f'{sender_name} перевел {transaction_value} FTC --> {getter_name}.')
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


@dp.message_handler(commands=['Бандит', 'бандит'])
async def bandit(message: types.Message):

    input_message = message.text.lower()
    check_user_existance(message)

    try:
        if len(input_message.split('/бандит ')) == 2 and '-' not in message.text:
            input_message = input_message.replace('/бандит ', '')
            print(input_message)

            bandit_command = {
                'Value':int(input_message),
            }

            # SQLite3 connection
            con = sqlite3.connect('users.db')
            cur = con.cursor()

            user_name = message.from_user.first_name
            user_unique_id = message.from_user.id
            user_balance = cur.execute(f'SELECT balance FROM users WHERE id = "{user_unique_id}"').fetchone()[0]

            if bandit_command['Value'] <= user_balance:

                bot_msg = await bot.send_message(message.chat.id, f'Bandit:\n'
                                                        f'X|X|X')

                time.sleep(0.4)
                r1 = random.randint(0, 9)
                await bot.edit_message_text(chat_id=bot_msg['chat']['id'], message_id=bot_msg['message_id'], text=f'Bandit:\n'
                                                        f'{r1}|X|X')
                time.sleep(0.4)
                r2 = random.randint(0, 9)
                await bot.edit_message_text(chat_id=bot_msg['chat']['id'], message_id=bot_msg['message_id'], text=f'Bandit:\n'
                                                        f'{r1}|{r2}|X')
                time.sleep(0.4)
                r3 = random.randint(0, 9)
                await bot.edit_message_text(chat_id=bot_msg['chat']['id'], message_id=bot_msg['message_id'], text=f'Bandit:\n'
                                                        f'{r1}|{r2}|{r3}')

                time.sleep(1.5)

                if r1 == r2 == r3:
                    cur.execute(
                        f'UPDATE users SET balance = "{user_balance + (bandit_command["Value"] * 10)}" WHERE id = "{user_unique_id}"')
                    con.commit()

                    time.sleep(0.8)
                    await bot.edit_message_text(chat_id=bot_msg['chat']['id'],
                                                message_id=bot_msg['message_id'],
                                                text=f'{user_name} выиграл {bandit_command["Value"] * 10} FTC!')
                elif r1 == r2 or r2 == r3 or r1 == r3:
                    cur.execute(
                        f'UPDATE users SET balance = "{user_balance + (bandit_command["Value"] * 10)}" WHERE id = "{user_unique_id}"')
                    con.commit()

                    time.sleep(0.8)
                    await bot.edit_message_text(chat_id=bot_msg['chat']['id'],
                                                message_id=bot_msg['message_id'],
                                                text=f'{user_name} выиграл {bandit_command["Value"] * 2} FTC!')
                else:
                    cur.execute(
                        f'UPDATE users SET balance = "{user_balance - bandit_command["Value"]}" WHERE id = "{user_unique_id}"')
                    con.commit()

                    time.sleep(0.8)
                    await bot.edit_message_text(chat_id=bot_msg['chat']['id'],
                                                message_id=bot_msg['message_id'],
                                                text=f'{user_name} проиграл {bandit_command["Value"]} FTC!')



            else:
                await message.reply(f'Не достаточно FTC.')


    except Exception:
        await message.reply(f'Данная команда не существует,\n'
                            f'попробуй написать:\n'
                            f'/Бандит кол-во FTC')




def main():
    create_users_bd()
    keep_alive()
    executor.start_polling(dp, skip_updates=True, reset_webhook=True)

if __name__ == '__main__':
    main()
