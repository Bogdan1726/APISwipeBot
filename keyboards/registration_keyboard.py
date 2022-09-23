from aiogram import types
from aiogram.utils.i18n import gettext as _


def get_register_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Зарегистрироватся")))
        ],
        [
            types.KeyboardButton(text=str(_("Редактировать email"))),
            types.KeyboardButton(text=str(_("Редактировать пароль")))
        ],
        [
            types.KeyboardButton(text=str(_("Редактировать имя"))),
            types.KeyboardButton(text=str(_("Редактировать фамилию"))),
        ],
        [
            types.KeyboardButton(text=str(_('Отмена')))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_back_register():
    buttons = [
        [
            types.KeyboardButton(text=str(_('Вернутся к регистрации')))
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
