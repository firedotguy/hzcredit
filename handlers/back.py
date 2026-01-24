from typing import cast

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from logger import get_logger

l = get_logger()
router = Router()

@router.callback_query(F.data == 'back_last')
async def back(callback: CallbackQuery):
    assert callback.message
    assert callback.bot
    assert callback.data

    l.info('callback back last')
    await cast(Message, callback.message).delete()

@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    l.info('cmd cancel')
    await cancel(state, message)

@router.callback_query(F.data == 'back')
async def cancel_callback(callback: CallbackQuery, state: FSMContext):
    assert callback.message
    l.info('callback back')
    await cancel(state, cast(Message, callback.message), True)

    await callback.answer()

async def cancel(state: FSMContext, message: Message, callback: bool = False):
    assert message.bot
    if await state.get_state() is None:
        l.error('nothing to cancel')
        await message.answer('Нечего отменять')
        return

    for message_id in (await state.get_data()).get('message_ids', []) + ([message.message_id] if not callback else []):
        l.debug('delete message %s', message_id)
        await message.bot.delete_message(message.chat.id, message_id)

    await state.set_state(None)
