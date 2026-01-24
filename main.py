from asyncio import run, CancelledError
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from logger import get_logger
from db import create_db, DBMiddleware
from handlers import base_router

l = get_logger()
load_dotenv()

TOKEN = getenv('TOKEN')
if TOKEN is None:
    l.critical('no token')
    quit()

bot = Bot(TOKEN, default=DefaultBotProperties(ParseMode.HTML))
dp = Dispatcher()
l.info('bot init')

create_db()

dp.include_routers(base_router)
dp.message.middleware(DBMiddleware())
dp.callback_query.middleware(DBMiddleware())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        run(main())
    except (KeyboardInterrupt, CancelledError):
        l.info('bot stop (cancelled by user)')