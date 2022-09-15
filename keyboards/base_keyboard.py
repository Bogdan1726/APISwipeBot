from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# buttons = [
#
#     [
#         types.KeyboardButton(text="Вход"),
#         types.KeyboardButton(text="Регистрация")
#     ],
#     types.KeyboardButton(test='test')
# ]
#
# keyboard = types.ReplyKeyboardMarkup(
#     keyboard=buttons,
#     resize_keyboard=True,
#     input_field_placeholder="Выберите, что вы хотите сделать"
# )

keyboard = ReplyKeyboardBuilder()
keyboard.row(
    types.KeyboardButton(text="Вход"),
    types.KeyboardButton(text="Регистрация")
)

keyboard.row(
    types.KeyboardButton(text='К выбору языка')
)

btn_cancel = [
    [types.KeyboardButton(text="Отмена")]
]
cancel = types.ReplyKeyboardMarkup(
    keyboard=btn_cancel,
    resize_keyboard=True
)

btn_language = [
    [
        types.KeyboardButton(text="Рус"),
        types.KeyboardButton(text="Укр")
    ]
]
language = types.ReplyKeyboardMarkup(
    keyboard=btn_language,
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
