from typing import cast

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm.session import Session

from logger import get_logger
from models import Trade
from keyboards import build_trades_kb, get_back_kb, new_trade_kb, get_trade_complete_kb, get_trade_kb
import crud

l = get_logger()
router = Router()


class NewTradeChange(StatesGroup):
    start = State()
    finish = State()


@router.message(F.text.lower() == 'трейды')
async def trades(message: Message, db: Session):
    l.info('text trades')
    trades = crud.get_trades(db)
    await message.answer(f'<b>Трейды:</b>{"\n<i>Нет активных трейдов</i>" if not trades else ""}', reply_markup=build_trades_kb(trades))


@router.callback_query(F.data == 'trade_my')
async def trade_my(callback: CallbackQuery, db: Session):
    assert callback.message
    l.info('callback my trades')

    user = crud.get_user(db, callback.from_user.id)
    if user is None:
        await callback.message.answer('Пользователь не найден')
        await callback.answer()
        return

    trades = crud.get_trades(db, False, trader_id=cast(int, user.id)) + crud.get_trades(db, False, purchaser_id=cast(int, user.id))
    if not trades:
        message = await callback.message.answer('<i>Нет трейдов</i>')
        await message.edit_reply_markup(reply_markup=get_back_kb(True))
        await callback.answer()
        return

    await callback.message.answer('<b>Ваши трейды:</b>', reply_markup=build_trades_kb(trades, True))
    await callback.answer()


@router.callback_query(F.data.regexp(r'^trade_\d+$'))
async def trade(callback: CallbackQuery, db: Session):
    assert callback.message
    assert callback.data
    l.info('callback trade %s', callback.data.split('_')[1])

    trade = crud.get_trade(db, int(callback.data.split('_')[1]))
    if trade is None:
        message = await callback.message.answer('Трейд не найден')
        await message.edit_reply_markup(reply_markup=get_back_kb(True))
        await callback.answer()
        return

    message = await callback.message.answer(
        f'''
<b>Информация о трейде</b>

<b>ID:</b> {trade.id}
<b>Дата создания:</b> {trade.created_at}
<b>Трейдер:</b> {trade.trader.name}
<b>Покупатель:</b> {trade.purchaser.name if trade.purchaser else "-"}

<b>Ресурсы для трейда:</b>
    <b>Трейдер:</b>
        <b>СЦК:</b> {trade.trading_amount or 0.0}
        <b>Звание:</b> {trade.trading_rank.name if trade.trading_rank else "-"}
    <b>Покупатель:</b>
        <b>СЦК:</b> {trade.purchasing_amount or 0.0}
        <b>Звание:</b> {trade.purchasing_rank.name if trade.purchasing_rank else "-"}

<b>Завершен:</b> {"Да" if cast(bool, trade.completed) else "Нет"}
<b>Дата завершения:</b> {trade.completed_at or "-"}
<b>Удален:</b> {"Да" if cast(bool, trade.deleted) else "Нет"}
        ''')
    await message.edit_reply_markup(reply_markup=get_trade_kb(cast(int, trade.id), trade.trader.user_id == callback.from_user.id))
    await callback.answer()


async def show_trade_new(message: Message, state: FSMContext):
    trade: Trade = (await state.get_data()).get('trade') or Trade()

    m = await message.answer(f'''
<b>Новый трейд</b>

<b>Вы отдаете:</b>
    [1] <b>СЦК:</b> {trade.trading_amount or 0.0}
    [2] <b>Звание:</b> {trade.trading_rank.name if trade.trading_rank else "-"}
<b>Вы получаете:</b>
    [3] <b>СЦК:</b> {trade.purchasing_amount or 0.0}
    [4] <b>Звание:</b> {trade.purchasing_rank.name if trade.purchasing_rank else "-"}
''', reply_markup=new_trade_kb)
    await state.update_data(trade=trade, trade_message_id=m.message_id)
    await state.set_state(NewTradeChange.start)


@router.callback_query(F.data == 'trade_new')
async def trade_new(callback: CallbackQuery, state: FSMContext):
    assert callback.message
    await show_trade_new(cast(Message, callback.message), state)
    await callback.answer()


@router.callback_query(F.data.regexp(r'^trade_new_(?:trader|purchaser)_(?:amount|rank)$'))
async def trade_new_update1(callback: CallbackQuery, db: Session, state: FSMContext):
    assert callback.message
    assert callback.data
    cdata = callback.data.split('_')[2:]
    l.info('callback new trade update person=%s item=%s', cdata[0], cdata[1])

    title = ''
    description = ''
    user = crud.get_user(db, callback.from_user.id)
    if user is None:
        await callback.message.answer('Пользователь не найден')
        await callback.answer()
        return

    if cdata[0] == 'trader' and cdata[1] == 'amount':
        title = 'ваши СЦК для трейда'
        description = 'Количество СЦК, которые вы отдадите покупателю'

    elif cdata[0] == 'trader' and cdata[1] == 'rank':
        if not user.ranks:
            l.error('no ranks for trade')
            await callback.message.answer('У вас нет званий для трейда!')
            await callback.answer()
            return

        title = 'ваше звание для трейда'
        description = 'Звание, которое вы отдадите покупателю'

    elif cdata[0] == 'purchaser' and cdata[1] == 'amount':
        title = 'СЦК покупателя для трейда'
        description = 'Количество СЦК, которые вам отдаст покупатель'

    elif cdata[0] == 'purchaser' and cdata[1] == 'rank':
        title = 'звание покупателя для трейда'
        description = 'Звание, которое вам отдаст покупатель'

    else:
        l.error('unknown person or item')
        return

    message = await callback.message.answer(
        f'''
<b>Введите {title}:</b>
{description}
<i>Отправьте /cancel или нажмите "Назад" чтобы отменить</i>
        ''', reply_markup=get_back_kb())
    await state.set_state(NewTradeChange.finish)
    await state.update_data(user=user, person=cdata[0], item=cdata[1], message_ids=[message.message_id])
    await callback.answer()


@router.message(NewTradeChange.finish, F.text)
async def trade_new_update2(message: Message, db: Session, state: FSMContext):
    assert message.from_user
    assert message.text
    assert message.bot
    data = await state.get_data()
    l.info('message new trade update value=%s', message.text)

    if data['item'] == 'amount':
        if not message.text.isdigit():
            l.error('wrong number for amount')
            new_message = await message.answer('Пожалуйста, введите число')
            await state.update_data(message_ids=data['message_ids'] + [new_message.message_id, message.message_id])
            return
        else:
            if data['person'] == 'trader':
                data['trade'].trading_amount = float(message.text)
            else:
                data['trade'].purchasing_amount = float(message.text)
    else:
        rank = crud.get_rank_by_name(db, message.text)
        if rank is None:
            new_message = await message.answer('Звание не найдено')
            await state.update_data(message_ids=data['message_ids'] + [new_message.message_id, message.message_id])
            return

        elif data['person'] == 'trader' and rank.owner_id != data['user'].id:
            new_message = await message.answer('У вас нету этого звания')
            await state.update_data(message_ids=data['message_ids'] + [new_message.message_id, message.message_id])
            return

        elif data['person'] == 'trader':
            data['trade'].trading_rank = rank
        else:
            data['trade'].purchasing_rank = rank

    for message_id in data['message_ids'] + [message.message_id, data['trade_message_id']]:
        await message.bot.delete_message(message.chat.id, message_id)

    await state.update_data(trade=data['trade'], message_ids=[])
    await show_trade_new(message, state)


@router.callback_query(F.data == 'trade_new_complete')
async def trade_new_complete(callback: CallbackQuery, state: FSMContext, db: Session):
    assert callback.message
    l.info('callback trade new complete')

    data = await state.get_data()
    if data['user']:
        data['trade'].trader_id = data['user'].id
    else:
        user = crud.get_user(db, callback.from_user.id)
        if user is None:
            await callback.message.answer('Пользователь не найден')
            await callback.answer()
            return
        data['trade'].trader_id = user.id

    trade = crud.create_trade(db, data['trade'])
    await state.clear()
    await cast(Message, callback.message).delete()

    await callback.message.answer(
        f'''
<b>Трейд создан!</b>

<b>ID:</b> {trade.id}
        ''', reply_markup=get_trade_complete_kb(cast(int, trade.id)))
    await callback.answer()


@router.callback_query(F.data.regexp(r'^trade_\d+_delete$'))
async def trade_delete(callback: CallbackQuery, db: Session):
    assert callback.data
    assert callback.message
    id = int(callback.data.split('_')[1])
    l.info('callback trade delete id=%s', id)

    trade = crud.get_trade(db, id)
    if trade is None:
        await callback.message.answer('Трейд не найден')
        await callback.answer()
        return

    if cast(bool, trade.completed):
        await callback.message.answer('Трейд уже завершен')
        await callback.answer()
        return

    if trade.purchaser:
        await callback.message.answer('У трейда уже есть покупатель')
        await callback.answer()
        return

    if cast(bool, trade.deleted):
        await callback.message.answer('Трейд уже удален')
        await callback.answer()
        return

    crud.delete_trade(db, id)
    await callback.message.answer('Трейд удален')
    await cast(Message, callback.message).delete()
    await callback.answer()


@router.callback_query(F.data.regexp(r'^trade_\d+_accept$'))
async def trade_accept(callback: CallbackQuery, db: Session):
    assert callback.data
    assert callback.message
    id = int(callback.data.split('_')[1])
    l.info('callback trade accept id=%s', id)

    trade = crud.get_trade(db, id)
    if trade is None:
        await callback.message.answer('Трейд не найден')
        await callback.answer()
        return

    if trade.purchaser is not None:
        await callback.message.answer('У трейда уже есть покупатель')
        await callback.answer()
        return

    if cast(bool, trade.deleted):
        await callback.message.answer('Трейд уже удален')
        await callback.answer()
        return

    user = crud.get_user(db, callback.from_user.id)
    if user is None:
        await callback.message.answer('Пользователь не найден')
        await callback.answer()
        return
    trade.purchaser = user


    if trade.trading_amount is not None and trade.trader.balance < trade.trading_amount:
        await callback.message.answer('У трейдера недостаточно СЦК')
        await callback.answer()
        return

    if trade.purchasing_amount is not None and trade.purchaser.balance < trade.purchasing_amount:
        await callback.message.answer('У вас недостаточно СЦК')
        await callback.answer()
        return

    if trade.trading_rank is not None and trade.trading_rank not in trade.trader.ranks:
        await callback.message.answer('У трейдера нет необходимого звания')
        await callback.answer()
        return

    if trade.purchasing_rank is not None and trade.purchasing_rank not in trade.purchaser.ranks:
        await callback.message.answer('У вас нет необходимого звания')
        await callback.answer()
        return

    crud.accept_trade(db, id, cast(int, user.id))

    if trade.trading_rank is not None:
        crud.transfer_rank(db, trade.trading_rank, cast(int, trade.purchaser_id))
    if trade.purchasing_rank is not None:
        crud.transfer_rank(db, trade.purchasing_rank, cast(int, trade.trader_id))
    if trade.trading_amount is not None:
        crud.make_transaction(db, cast(float, trade.trading_amount), trade.trader, trade.purchaser)
    if trade.purchasing_amount is not None:
        crud.make_transaction(db, cast(float, trade.purchasing_amount), trade.purchaser, trade.trader)

    await callback.message.answer(
        f'''
<b>Трейд принят!</b>

<b>Снято СЦК:</b> {trade.purchasing_amount or 0.0}
<b>Получено СЦК:</b> {trade.trading_amount or 0.0}

<b>Отдано звание:</b> {trade.purchasing_rank.name if trade.purchasing_rank else "-"}
<b>Получено звание:</b> {trade.trading_rank.name if trade.trading_rank else "-"}
        ''', reply_markup=get_back_kb(True))
    await callback.answer()
