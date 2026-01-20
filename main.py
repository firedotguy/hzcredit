from asyncio import run, CancelledError
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions, Message, KeyboardButton, ReplyKeyboardMarkup

from logger import get_logger
from db import get_db, create_db
import crud

l = get_logger()
load_dotenv()

TOKEN = getenv('TOKEN')
if TOKEN is None:
    l.critical('no token')
    quit()

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
l.info('bot init')

create_db()
db = get_db()
l.info('db init')


@dp.message(Command('start'))
async def start(message: Message):
    user_data = message.from_user
    assert user_data is not None

    l.info('cmd /start')
    user = crud.get_user(db, user_data.id)
    if not user:
        l.warning('user not found')
        user = crud.create_user(db, user_data.first_name, user_data.id)
    else:
        l.info('found user id=%s', user.id)

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='История'),
                KeyboardButton(text='Перевод')
            ],
            [
                KeyboardButton(text='Звания'),
                KeyboardButton(text='Трейды')
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
f'''<b>Добро пожаловать в хз бота</b>

<b>Баланс:</b> {user.balance}сцк
<b>ID:</b> {user.id}

<i>Исходный код бота:</i> <a href="https://github.com/firedotguy/hzcredit">GitHub</a>
<i>Версия <b>0.1.0</b></i>
''', link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=kb)


@dp.message(F.text.lower() == 'история')
async def history(message: Message):
    await message.answer('Панель в разработке')


@dp.message(F.text.lower() == 'перевод')
async def new_transaction(message: Message):
    await message.answer('Панель в разработке')


@dp.message(F.text.lower() == 'звания')
async def rank(message: Message):
    await message.answer('Панель в разработке')


@dp.message(F.text.lower() == 'трейды')
async def trades(message: Message):
    await message.answer('Панель в разработке')



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        run(main())
    except (KeyboardInterrupt, CancelledError):
        l.info('bot stop (cancelled by user)')