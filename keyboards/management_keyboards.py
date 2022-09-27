from aiogram import types
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


def get_profile_edit_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Редактировать email"))),
            types.KeyboardButton(text=str(_("Редактировать телефон"))),
        ],
        [
            types.KeyboardButton(text=str(_("Редактировать имя"))),
            types.KeyboardButton(text=str(_("Редактировать фамилию"))),
        ],
        [
            types.KeyboardButton(text=str(_('Установить новое фото профиля')))
        ],
        [
            types.KeyboardButton(text=str(_('Назад в Профиль')))
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
            types.KeyboardButton(text=str(_('Отменить редактирование')))
        ]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_profile_cancel():
    buttons = [
        [
            types.KeyboardButton(text=str(_('Назад в Профиль')))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_edit_ads_keyboard(pk):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=_("Редактировать объявления"),
        callback_data=f"edit_ads_{pk}")
    )
    return builder.as_markup()
