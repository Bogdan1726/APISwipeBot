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
