from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

btn_menu = [
    [
        types.KeyboardButton(text="Главное меню"),
        types.KeyboardButton(text="Выход")
    ]
]

menu = types.ReplyKeyboardMarkup(
    keyboard=btn_menu,
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
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


btn_auth = [
    [
        types.KeyboardButton(text="Авторизоватся"),
        types.KeyboardButton(text="Отмена")
    ]
]
auth = types.ReplyKeyboardMarkup(
    keyboard=btn_auth,
    resize_keyboard=True
)