from aiogram import types

buttons = [

    [
        types.KeyboardButton(text="Вход"),
        types.KeyboardButton(text="Регистрация")
    ]
]

keyboard = types.ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder="Выберите, что вы хотите сделать"
)

btn_cancel = [
    [types.KeyboardButton(text="Отмена")]
]
cancel = types.ReplyKeyboardMarkup(
    keyboard=btn_cancel,
    resize_keyboard=True
)
