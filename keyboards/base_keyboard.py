from aiogram import types
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __


def get_base_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Вход"))),
            types.KeyboardButton(text=str(_("Регистрация")))
        ],
        [types.KeyboardButton(text=str(_("К выбору языка")))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_language_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(__("Русский"))),
            types.KeyboardButton(text=str(__("Украинский")))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_cancel_group_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Отмена"))),
            types.KeyboardButton(text=str(_('Назад')))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_cancel_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_('Отмена')))
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
