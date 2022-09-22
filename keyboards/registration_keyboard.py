from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --//--

reg_keyboards = [
    [
        types.KeyboardButton(text="Зарегистрироватся")
    ],
    [
        types.KeyboardButton(text="Редактировать email"),
        types.KeyboardButton(text="Редактировать пароль")
    ],
    [
        types.KeyboardButton(text="Редактировать имя"),
        types.KeyboardButton(text="Редактировать фамилию"),
    ],
    [
        types.KeyboardButton(text='Отмена')
    ]
]

reg_keyboard = types.ReplyKeyboardMarkup(
    keyboard=reg_keyboards,
    reg_keyboards=True
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


reg_data = [
    [
        types.KeyboardButton(text='Вернутся к регистрации')
    ]
]

to_reg_data = types.ReplyKeyboardMarkup(
    keyboard=reg_data,
    resize_keyboard=True
)