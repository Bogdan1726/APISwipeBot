from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

# types.KeyboardButton(text="Запросить геолокацию", request_location=True),
# types.KeyboardButton(text="Запросить контакт", request_contact=True)

btn_language = [
    [
        types.KeyboardButton(text="Русский"),
        types.KeyboardButton(text="Украинский")
    ]

]
language = types.ReplyKeyboardMarkup(
    keyboard=btn_language,
    resize_keyboard=True
)

keyboard = ReplyKeyboardBuilder()
keyboard.row(
    types.KeyboardButton(text="Вход"),
    types.KeyboardButton(text="Регистрация")
)

keyboard.row(
    types.KeyboardButton(text='К выбору языка')
)

btn_cancel = [
    [
        types.KeyboardButton(text="Отмена"),
        types.KeyboardButton(text='Назад')
    ]
]
cancel = types.ReplyKeyboardMarkup(
    keyboard=btn_cancel,
    resize_keyboard=True
)

keyboards = [
    [
        types.KeyboardButton(text='Отмена')
    ]
]

cancel_keyboard = types.ReplyKeyboardMarkup(
    keyboard=keyboards,
    resize_keyboard=True
)
