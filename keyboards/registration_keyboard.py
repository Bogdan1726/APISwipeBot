from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --//--
reg_keyboard = ReplyKeyboardBuilder()
reg_keyboard.row(
    types.KeyboardButton(text="Зарегистрироватся"),
    types.KeyboardButton(text="Изменить данные")
)

reg_keyboard.row(
    types.KeyboardButton(text='Отмена')
)
# --//--

# --//--
buttons = [
    [
        types.KeyboardButton(text='Отмена'),
        types.KeyboardButton(text='Назад')
    ],
]
reg_keyboard_edit = types.ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
)
# --//--


# reg_keyboard = ReplyKeyboardBuilder()
# reg_keyboard.add(
#     types.KeyboardButton(text="Зарегистрироватся")
# )
# reg_keyboard.add(
#     types.KeyboardButton(text="Изменить данные")
# )
# reg_keyboard.add(
#     types.KeyboardButton(text="Отмена")
# )
# reg_keyboard.adjust(3)
