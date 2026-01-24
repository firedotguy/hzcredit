from typing import cast

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Rank, User, Trade

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='История'),
            KeyboardButton(text='Перевод')
        ],
        [
            KeyboardButton(text='Звания'),
            KeyboardButton(text='Трейды')
        ],
        [
            KeyboardButton(text='Конкурсы'),
            KeyboardButton(text='Топ')
        ]
    ],
    resize_keyboard=True
)


def build_ranks_kb(ranks: list[Rank]):
    builder = InlineKeyboardBuilder()
    for rank in ranks:
        builder.row(InlineKeyboardButton(text=str(rank.name), callback_data=f'rank_{rank.id}'))
    return builder.as_markup()

def build_users_kb(users: list[User]):
    builder = InlineKeyboardBuilder()
    for i, user in enumerate(users, 1):
        builder.row(InlineKeyboardButton(text=f'{i}: {user.name} ({user.balance} сцк)', callback_data=f'user_{user.id}'))
    return builder.as_markup()


def get_back_kb(last: bool = False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=f'back_last' if last else 'back')
            ]
        ]
    )


def build_trades_kb(trades: list[Trade], message_id: int | None = None):
    builder = InlineKeyboardBuilder()
    for trade in trades:
        trading = 'Ничего'
        purchasing = 'Ничего'

        if trade.trading_rank_id is not None:
            trading = trade.trading_rank.name
            if trade.trading_amount is not None:
                trading += f' + {trade.trading_amount} сцк'
        elif trade.trading_amount is not None:
            trading = f'{trade.trading_amount} сцк'

        if trade.purchasing_rank_id is not None:
            purchasing = trade.purchasing_rank.name
            if trade.purchasing_amount is not None:
                purchasing += f' + {trade.purchasing_amount} сцк'
        elif trade.purchasing_amount is not None:
            purchasing = f'{trade.purchasing_amount} сцк'

        completed = ''
        if cast(bool, trade.completed):
            completed = '[ЗАВЕРШЕН] '

        builder.row(InlineKeyboardButton(text=f'{completed}{trading} -> {purchasing}', callback_data=f'trade_{trade.id}'))
    # if not trades:
    #     builder.row(InlineKeyboardButton(text='Нет трейдов', callback_data='trade_no'))
    builder.row(InlineKeyboardButton(text='Создать трейд', callback_data='trade_new'))
    if message_id:
        builder.add(get_back_kb(True).inline_keyboard[0][0])
    else:
        builder.add(InlineKeyboardButton(text='Мои трейды', callback_data='trade_my'))
    return builder.as_markup()

new_trade_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить [1]', callback_data='trade_new_trader_amount'),
            InlineKeyboardButton(text='Изменить [2]', callback_data='trade_new_trader_rank')
        ],
        [
            InlineKeyboardButton(text='Изменить [3]', callback_data='trade_new_purchaser_amount'),
            InlineKeyboardButton(text='Изменить [4]', callback_data='trade_new_purchaser_rank')
        ],
        [
            InlineKeyboardButton(text='Опубликовать', callback_data='trade_new_complete'),
        ],
        get_back_kb(True).inline_keyboard[0]
    ]
)


def get_trade_complete_kb(trade_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Открыть трейд', callback_data=f'trade_{trade_id}')
            ],
            get_back_kb(True).inline_keyboard[0]
        ]
    )


def get_trade_kb(trade_id: int, owner: bool = False):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Удалить', callback_data=f'trade_{trade_id}_delete')
            ] if owner else [
                InlineKeyboardButton(text='Принять', callback_data=f'trade_{trade_id}_accept')
            ],
            get_back_kb(True).inline_keyboard[0]
        ]
    )