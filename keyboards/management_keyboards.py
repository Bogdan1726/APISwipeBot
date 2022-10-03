from enum import Enum

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
            types.KeyboardButton(text=_("Адрес")),
            types.KeyboardButton(text=_("Описание")),
            types.KeyboardButton(text=_("Стоимость"))
        ],
        [
            types.KeyboardButton(text=_("Общая площадь")),
            types.KeyboardButton(text=_("Площадь кухни")),
            types.KeyboardButton(text=_("Планировка"))
        ],
        [
            types.KeyboardButton(text=_('Вид права')),
            types.KeyboardButton(text=_('Количество комнат')),
            types.KeyboardButton(text=_('Жилое состояние'))
        ],
        [
            types.KeyboardButton(text=_('Назад в Мои обьявления'))
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


# region edit ads

class AdsData(str, Enum):
    ban = "ban"
    kick = "kick"
    warn = "warn"


class MyCallback(CallbackData, prefix="ads"):
    pk: int
    key: str


def get_edit_ads_keyboard(
        pk):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=_("Редактировать объявления"),
        callback_data=MyCallback(pk=pk, key='edit_ads').pack()
    ))
    return builder.as_markup()


def edit_ads_layout_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Студия, санузел"))),
            types.KeyboardButton(text=str(_("Классическая"))),
        ],
        [
            types.KeyboardButton(text=str(_("Европланировка"))),
            types.KeyboardButton(text=str(_("Свободная"))),
        ],
        [types.KeyboardButton(text=str(_('Отменить редактирование')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def edit_ads_founding_document_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Собственность"))),
            types.KeyboardButton(text=str(_("Свидетельство о праве на наследство"))),
        ],
        [types.KeyboardButton(text=str(_('Отменить редактирование')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def edit_ads_condition_keyboard():
    buttons = [
        [
            types.KeyboardButton(text=str(_("Черновая"))),
            types.KeyboardButton(text=str(_("Ремонт от застройщика"))),
            types.KeyboardButton(text=str(_("В жилом состоянии"))),
        ],
        [types.KeyboardButton(text=str(_('Отменить редактирование')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


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


# region announcement

class AnnouncementCallback(CallbackData, prefix="announcement"):
    key: str
    pk: int


def get_announcement_keyboard(pk):
    buttons = [
        [
            types.InlineKeyboardButton(
                text=_("Предыдущее"),
                callback_data=AnnouncementCallback(key='go-previous', pk=pk).pack()
            ),
            types.InlineKeyboardButton(
                text=_("Cледующее"),
                callback_data=AnnouncementCallback(key='go-next', pk=pk).pack()
            )
        ],
        [
            types.InlineKeyboardButton(
                text=_("Показать геолокацию"),
                callback_data=AnnouncementCallback(key='geolocation', pk=pk).pack()
            )
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_announcement_back_keyboard():
    buttons = [
        [types.KeyboardButton(text=str(_('Назад в Главное меню')))]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
# endregion announcement
