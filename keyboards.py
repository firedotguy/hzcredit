from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='История'),
            KeyboardButton(text='Перевод')
        ],
        [
            KeyboardButton(text='Звания'),
            KeyboardButton(text='Трейды'),
            KeyboardButton(text='Топ')
        ]
    ],
    resize_keyboard=True
)