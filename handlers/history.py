from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.lower() == 'история')
async def history(message: Message):
    await message.answer('У вас еще не было транзакций')