from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data.regexp(r'back_\d+'))
async def back(callback: CallbackQuery):
    assert callback.message
    assert callback.bot
    assert callback.data
    await callback.bot.delete_message(callback.message.chat.id, int(callback.data.split('_')[1]))