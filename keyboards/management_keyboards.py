from aiogram import types
from aiogram.filters.callback_data import CallbackData
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


def get_my_ads_keyboards():
    buttons = [
        [
            types.KeyboardButton(text=str(_('Назад в Профиль'))),
            types.KeyboardButton(text=str(_('Добавить объявление')))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def get_profile_edit_ads():
    buttons = [
        [
            types.KeyboardButton(text=str("Адрес")),
            types.KeyboardButton(text=str("Описание")),
            types.KeyboardButton(text=str("Стоимость"))
        ],
        [
            types.KeyboardButton(text=str("Общая площадь")),
            types.KeyboardButton(text=str("Площадь кухни")),
            types.KeyboardButton(text=str("Планировка"))
        ],
        [
            types.KeyboardButton(text=str('Вид права')),
            types.KeyboardButton(text=str('Количество комнат')),
            types.KeyboardButton(text=str('Жилое состояние'))
        ],
        [
            types.KeyboardButton(text=str('Назад в Мои обьявления'))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


# region edit ads
class MyCallback(CallbackData, prefix="ads"):
    pk: int
    key: str


def get_edit_ads_keyboard(pk):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=_("Редактировать объявления"),
        callback_data=MyCallback(pk=pk, key='edit_ads').pack()
    ))
    return builder.as_markup()


# endregion edit ads


# region add ads

def add_ads_purpose_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Дом"))),
            types.KeyboardButton(text=str(_("Квартира"))),
        ],
        [
            types.KeyboardButton(text=str(_("Коммерческие помещения"))),
            types.KeyboardButton(text=str(_("Офисное помещение"))),
        ],
        [types.KeyboardButton(text=str(_('Вернутся к объявлениям')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def add_ads_condition_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Черновая"))),
            types.KeyboardButton(text=str(_("Ремонт от застройщика"))),
            types.KeyboardButton(text=str(_("В жилом состоянии"))),
        ],
        [
            types.KeyboardButton(text=str(_("Назад")))
        ],
        [
            types.KeyboardButton(text=str(_('Вернутся к объявлениям')))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def add_ads_house_keyboard():
    buttons = [
        [
            types.KeyboardButton(text="ЖК 1"),
            types.KeyboardButton(text="ЖК 2"),
            types.KeyboardButton(text="ЖК 3")
        ],
        [
            types.KeyboardButton(text="ЖК 4"),
            types.KeyboardButton(text="ЖК 5")
        ],
        [
            types.KeyboardButton(text=str(_("Назад")))
        ],

        [
            types.KeyboardButton(text=str(_('Вернутся к объявлениям')))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def add_ads_back_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_('Вернутся к объявлениям'))),
            types.KeyboardButton(text=str(_("Назад")))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def add_ads_finish():
    buttons = [
        [
            types.KeyboardButton(text=str(_('Добавить')))
        ],
        [
            types.KeyboardButton(text=str(_('Вернутся к объявлениям'))),
            types.KeyboardButton(text=str(_("Назад")))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

# endregion add ads
