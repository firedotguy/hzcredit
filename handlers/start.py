from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import LinkPreviewOptions, Message, KeyboardButton, ReplyKeyboardMarkup

from logger import get_logger
from db import Session
from keyboards import main_kb
import crud

l = get_logger()
router = Router()

@router.message(Command('start'))
async def start(message: Message, db: Session):
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
        f'''
<b>Добро пожаловать в хз бота</b>

<b>Баланс:</b> {user.balance}сцк
<b>ID:</b> {user.id}

<i>Исходный код бота:</i> <a href="https://github.com/firedotguy/hzcredit">GitHub</a>
<i>Версия <b>0.1.0</b></i>
        ''', link_preview_options=LinkPreviewOptions(is_disabled=True), reply_markup=main_kb)