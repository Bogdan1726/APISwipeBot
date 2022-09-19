from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ads = types.KeyboardButton(text="Объявления"),
# profile = types.KeyboardButton(text="Профиль")
# logout = types.KeyboardButton(text='Выход')

menu = ReplyKeyboardBuilder()
menu.row(
    types.KeyboardButton(text="Объявления"),
    types.KeyboardButton(text="Профиль")
)
menu.row(types.KeyboardButton(text='Выход'))


profile_buttons = [
    [
        types.InlineKeyboardButton(text='Мои обьявления', callback_data="num_decr"),
        types.InlineKeyboardButton(text='Редактировать профиль', callback_data="num_dec")
    ]
]
profile = types.InlineKeyboardMarkup(inline_keyboard=profile_buttons)

