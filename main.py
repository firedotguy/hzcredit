from asyncio import run, CancelledError
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

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
async def cmd_start(message: types.Message):
    user_data = message.from_user
    assert user_data is not None

    l.info('cmd /start')
    user = crud.get_user(db, user_data.id)
    if not user:
        l.warning('user not found')
        user = crud.create_user(db, user_data.first_name, user_data.id)
    else:
        l.info('found user id=%s', user.id)

    await message.answer(
f'''<b>Добро пожаловать в хз бота</b>\n
<b>Баланс:</b> {user.balance}сцк
<b>ID:</b> {user.id}
''')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        run(main())
    except (KeyboardInterrupt, CancelledError):
        l.info('bot stop (cancelled by user)')