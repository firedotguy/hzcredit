from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.orm.session import Session

from keyboards import build_ranks_kb, get_back_kb
from logger import get_logger
import crud

l = get_logger()
router = Router()

@router.message(F.text.lower() == 'звания')
async def rank(message: Message, db: Session):
    assert message.from_user
    l.info('text ranks')

    user = crud.get_user(db, message.from_user.id)
    if user is None:
        l.error('user not found')
        await message.answer('Пользователь не найден')
        return

    if not user.ranks:
        l.warning('user has not ranks')
        await message.answer('У вас нет званий')
        return

    await message.answer('<b>Ваши звания:</b>', reply_markup=build_ranks_kb(user.ranks))


@router.callback_query(F.data.regexp(r'^rank_\d+$'))
async def callback_rank(callback: CallbackQuery, db: Session):
    assert callback.message
    assert callback.data
    l.info('callback rank %s', callback.data.split('_')[1])

    rank = crud.get_rank(db, int(callback.data.split('_')[1]))

    if rank is None:
        await callback.message.answer('Звание не найдено')
        await callback.answer()
        return

    message = await callback.message.answer(
        f'''
<b>Информация о звании</b>

<b>ID:</b> {rank.id}
<b>Название:</b> {rank.name}
<b>Владелец:</b> {rank.owner.name}
<b>Дата создания:</b> {rank.created_at}
<b>Дата получения:</b> {rank.owned_at or "-"}
        ''')
    await message.edit_reply_markup(reply_markup=get_back_kb(True))
    await callback.answer()
