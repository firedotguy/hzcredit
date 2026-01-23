from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text.lower() == 'трейды')
async def trades(message: Message):
    await message.answer('Панель в разработке')