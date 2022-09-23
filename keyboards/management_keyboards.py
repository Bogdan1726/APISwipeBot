from aiogram import types
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


def get_main_menu_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Объявления"))),
            types.KeyboardButton(text=str(_("Профиль")))
        ],
        [types.KeyboardButton(text=str(_('Выход')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_profile_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Мои обьявления"))),
            types.KeyboardButton(text=str(_("Редактировать профиль")))
        ],
        [types.KeyboardButton(text=str(_('Назад в Главное меню')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
