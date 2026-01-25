from typing import cast

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm.session import Session

from keyboards import build_transactions_kb, get_back_kb
from logger import get_logger
import crud

l = get_logger()
router = Router()

@router.message(F.text.lower() == 'перевод')
async def new_transaction(message: Message):
    await message.answer('Переводы пока недоступны')


@router.message(F.text.lower() == 'история')
async def history(message: Message, db: Session):
    assert message.from_user
    l.info('text history')

    user = crud.get_user(db, message.from_user.id)
    if user is None:
        await message.answer('Пользователь не найден')
        return

    if not user.transactions:
        await message.answer('У вас еще не было транзакций')
        return

    await message.answer('<b>Ваши транзакции:</b>', reply_markup=build_transactions_kb(user.transactions, cast(int, user.id)))