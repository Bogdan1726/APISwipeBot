from aiogram import types
from aiogram.utils.i18n import gettext as _


def get_auth_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Войти"))),
            types.KeyboardButton(text=str(_("Отмена")))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
