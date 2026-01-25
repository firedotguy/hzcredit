from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm.session import Session

from keyboards import build_ranks_kb, get_back_kb
from logger import get_logger
import crud

l = get_logger()
router = Router()

@router.message(F.text.lower() == 'конкурсы')
async def rank(message: Message, db: Session):
    await message.answer('Конкурсы пока недоступны')