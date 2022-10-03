from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery, ReplyKeyboardRemove
from yarl import URL
from api_requests.user import AdsApiClient
from database.requests import is_authenticated
from keyboards import base_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from keyboards.management_keyboards import MyCallback, AnnouncementCallback
from settings.config import HOST, DEFAULT_IMAGE
from settings.states import BaseStates, AuthenticationStates, AnnouncementStates

router = Router()

domain = URL.build(
    scheme='http',
    host=HOST,
)

# region image


def get_image_ads(url=None):
    """
    return default image if url is None
    """
    image = URLInputFile(
        DEFAULT_IMAGE,
        filename="image")
    if url:
        image.url = url
    return image


def get_image(path=None):
    """
    return default image if path is None
    """
    image = URLInputFile(
        DEFAULT_IMAGE,
        filename="image")
    if path:
        image.url = str(domain) + str(path)
    return image

# endregion image


# region feed
class NegativeIndexError(Exception):
    pass


user_data = {}


@router.message(AuthenticationStates.main_menu, F.text.lower() == __("объявления"))
async def announcement_feed(message: Message, state: FSMContext):
    user = message.from_user.id
    ads_client = AdsApiClient(user)
    if is_authenticated(user):
        await message.answer(
            _('Добро пожаловать в ленту объявлений'),
            reply_markup=management_keyboards.get_announcement_back_keyboard()
        )
        await state.set_state(AnnouncementStates.ads)
        data = await ads_client.get_announcement_feed()
        user_data[message.from_user.id] = 0
        if data:
            detail_data = data.get('data')
            await message.answer_photo(
                photo=get_image_ads(url=detail_data[user_data[message.from_user.id]].get('preview_image')),
                caption=
                _("Адрес - {address}\n"
                  "Площадь - {area} кв.м\n"
                  "Цена - {price} грн\n"
                  ).format(
                    address=detail_data[user_data[message.from_user.id]].get('address'),
                    area=detail_data[user_data[message.from_user.id]].get('area'),
                    price=detail_data[user_data[message.from_user.id]].get('price')
                ), parse_mode="HTML",
                reply_markup=management_keyboards.get_announcement_keyboard(int(user))
            )
        else:
            await message.answer(
                _('Лента пуста')
            )
    else:
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.get_base_keyboard())
        await state.set_state(BaseStates.auth)


@router.callback_query(AnnouncementCallback.filter(F.key.startswith('go-')))
async def announcement_next(callback: CallbackQuery, callback_data: MyCallback):
    ads_client = AdsApiClient(callback_data.pk)
    data = await ads_client.get_announcement_feed()
    try:
        if callback_data.key == 'go-next':
            user_data[callback_data.pk] += 1
        elif callback_data.key == 'go-previous':
            user_data[callback_data.pk] -= 1
        if data:
            detail_data = data.get('data')
            try:
                if user_data[callback_data.pk] < 0:
                    raise NegativeIndexError
                if detail_data[user_data[callback_data.pk]].get('price'):
                    await callback.message.answer_photo(
                        photo=get_image_ads(url=detail_data[user_data[callback_data.pk]].get('preview_image')),
                        caption=
                        _("Адрес - {address}\n"
                          "Площадь - {area} кв.м\n"
                          "Цена - {price} грн\n"
                          ).format(
                            address=detail_data[user_data[callback_data.pk]].get('address'),
                            area=detail_data[user_data[callback_data.pk]].get('area'),
                            price=detail_data[user_data[callback_data.pk]].get('price')
                        ), parse_mode="HTML",
                        reply_markup=management_keyboards.get_announcement_keyboard(int(callback_data.pk))
                    )
                else:
                    await callback.message.answer_photo(
                        photo=get_image(path=detail_data[user_data[callback_data.pk]].get('preview_image')),
                        caption=
                        _("Название - {name}\n"
                          "Адрес - {address} кв.м\n"
                          ).format(
                            address=detail_data[user_data[callback_data.pk]].get('address'),
                            name=detail_data[user_data[callback_data.pk]].get('name'),
                        ), parse_mode="HTML",
                        reply_markup=management_keyboards.get_announcement_keyboard(int(callback_data.pk))
                    )
            except IndexError:
                await callback.message.answer(
                    _('Это было последнее объявление')
                )
                user_data[callback_data.pk] -= 1
            except NegativeIndexError:
                await callback.message.answer(
                    _('Это было первое объявление')
                )
                user_data[callback_data.pk] += 1
    except KeyError:
        await callback.message.answer(
            _('Произошла ошибка вернитесь перезапустите бота командой\n'
              '/start'),
            reply_markup=ReplyKeyboardRemove()
        )
    await callback.answer()


@router.callback_query(AnnouncementCallback.filter(F.key == "geolocation"))
async def get_announcement_geolocation(callback: CallbackQuery):
    await callback.message.answer_location(
        latitude=46.468851871374525, longitude=30.710127484338713
    )
    await callback.answer()

# endregion feed
