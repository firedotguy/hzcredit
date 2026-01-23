from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Rank

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

def get_back_kb(message_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Назад', callback_data=f'back_{message_id}')
            ]
        ]
    )