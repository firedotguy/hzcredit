from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.orm.session import Session

import crud
from logger import get_logger
from keyboards import build_users_kb

l = get_logger()
router = Router()

@router.message(F.text.lower() == 'топ')
async def rank(message: Message, db: Session):
    l.info('text top')
    users = crud.get_user_top(db)
    if not users:
        await message.answer('Пусто')
        return

    await message.answer('<b>Топ пользователей:</b>', reply_markup=build_users_kb(users))