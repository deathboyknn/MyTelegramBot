import json
import time
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.types import Message
from aiogram import executor

import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from db import Database

from engine import get_answers
from config import get_tg_token
import config as cfg
bot = Bot(get_tg_token())
#bot = Bot(token=cfg.TG_TOKEN)
db = Database("data.db")

dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

# updater = Updater(token=get_tg_token(), use_context=True)
# dispatcher = updater.dispatcher


# def messages_handler(update: Update, context: CallbackContext):
#     try:
#         msg = update.message.text
#     except AttributeError:
#         return
#     try:
#         answers = get_answers(msg)
#         context.bot.send_message(
#             chat_id=update.effective_chat.id, text=answers["message"]
#         )
#         if answers["channel"]:
#             if answers["cl"] == 8:
#                 context.bot.send_message(
#                     chat_id=-1001403887087, text=answers["message"]
#                 )
#             if answers["cl"] == 9:
#                 context.bot.send_message(
#                     chat_id=-1001599892206, text=answers["message"]
#                 )
#             if answers["cl"] == 10:
#                 context.bot.send_message(
#                     chat_id=-1001783255653, text=answers["message"]
#                 )
#             if answers["cl"] == 11:
#                 context.bot.send_message(
#                     chat_id=-1001693528441, text=answers["message"]
#                 )
#     except json.decoder.JSONDecodeError:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="Ты мне какую что хрень кинул, перепроверь. " "Или админу напиши",
#         )


# echo_handler = MessageHandler(Filters.text & (~Filters.command), messages_handler)
# dispatcher.add_handler(echo_handler)
# updater.start_polling()
'''
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    qq=message.from_user.id
    tt=message.from_user.username
    if (not db.user_exists(qq)):
        gg=False
        await bot.send_messag   e(message.from_user.id, f"{tt} иди нах или купи доступ")
        await bot.send_message(2050755561, f"Ник: {tt} \nID: {qq} не состоит в базе, а лезет")
        logging.info(f'Ник: {tt} \nID: {qq} не состоит в базе, а лезет')
    else:
        gg=True
        await bot.send_message(2050755561, f"Ник: {tt} \nID: {qq} состоит в базе")
        logging.info(f'Ник: {tt} \nID: {qq} состоит в базе')
        await bot.send_message(qq, f"Ник: {tt} \nID: {qq} состоит в базе")


@dp.message_handler(commands=['add'])
async def start(message: types.Message):
    qq = message.from_user.id
    tt = message.from_user.username
    if qq!=2050755561:
        await bot.send_message(2050755561, f"Ты не админ, иди нах")
    else:
        @dp.message_handler(filters.Text)
        async def start(message: types.Message):
            await bot.send_message(2050755561, f"Введите nickname и user_id")
            ss = message.text
            hh=ss.split()
            db.add_user(hh[1], hh[0])
            await bot.send_message(2050755561, f"Добавлен новый пользователь: {hh[0]} \nID: {hh[1]}")
            await bot.send_message(hh[1], f"Вы стали новым участником")
            logging.info(f'Добавлен новый пользователь: {hh[0]} \nID: {hh[1]}"')
'''
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"{message.from_user.username} иди нах или купи доступ")

@dp.message_handler(filters.Text)
async def messages_handler(message: types.Message):
    msg = message.text
    if db.user_exists(message.from_user.id):
        try:
            answers = get_answers(msg)
            await bot.send_message(chat_id=message.chat.id, text=answers['message'])
        except json.decoder.JSONDecodeError:
            await bot.send_message(chat_id=message.chat.id, text="Неверный айди")
        await bot.send_message(2050755561, f"Ник: {message.from_user.username} \nID: {message.from_user.id} состоит в базе")
        logging.info(f'Ник: {message.from_user.username} \nID: {message.from_user.id} состоит в базе')
    else:
        await bot.send_message(message.from_user.id, f"{message.from_user.username} иди нах или купи доступ")
        await bot.send_message(2050755561, f"Ник: {message.from_user.username} \nID: {message.from_user.id} не состоит в базе, а лезет")
        logging.info(f'Ник: {message.from_user.username} \nID: {message.from_user.id} не состоит в базе, а лезет')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
