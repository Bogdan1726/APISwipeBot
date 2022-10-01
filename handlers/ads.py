from aiogram import Router, F
from aiogram.types import Message, URLInputFile, CallbackQuery
from yarl import URL
from api_requests.user import AdsApiClient
from database.requests import is_authenticated
from keyboards import base_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from keyboards.management_keyboards import MyCallback, AnnouncementCallback
from settings.config import HOST, DEFAULT_IMAGE
from settings.states import BaseStates


router = Router()

domain = URL.build(
    scheme='http',
    host=HOST,
)


# region image

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

@router.message(F.text.lower() == __("объявления"))
async def announcement_feed(message: Message, state: FSMContext):
    user = message.from_user.id
    ads_client = AdsApiClient(user)
    if is_authenticated(user):
        await message.answer(
            _('Добро пожаловать в ленту объявлений'),
            reply_markup=management_keyboards.get_announcement_back_keyboard()
        )
        data = await ads_client.get_announcement_feed()
        if data:
            detail_data = data.get('data')
            await message.answer_photo(
                photo=get_image(path=data.get('preview_image')),
                caption=
                _("Адрес - {address}\n"
                  "Площадь - {area} кв.м\n"
                  "Цена - {price} грн\n"
                  ).format(
                    address=detail_data[0].get('address'),
                    area=detail_data[0].get('area'),
                    price=detail_data[0].get('price')
                ), parse_mode="HTML",
                reply_markup=management_keyboards.get_announcement_keyboard(int(user))
            )
        else:
            await message.answer(
                _('Errro data')
            )
    else:
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.get_base_keyboard())
        await state.set_state(BaseStates.start)


@router.callback_query(AnnouncementCallback.filter(F.key == "geolocation"))
async def get_announcement_geolocation(callback: CallbackQuery, callback_data: MyCallback):
    await callback.message.answer_location(
        latitude=48.47557630292473, longitude=34.947974998733024
    )
    await callback.answer()


@router.callback_query(AnnouncementCallback.filter(F.key == "next"))
async def announcement_next(callback: CallbackQuery, callback_data: MyCallback):
    ads_client = AdsApiClient(callback_data.pk)
    data = await ads_client.get_announcement_feed()
    if data:
        detail_data = data.get('data')
        await callback.message.answer_photo(
            photo=get_image(path=data.get('preview_image')),
            caption=
            _("Адрес - {address}\n"
              "Площадь - {area} кв.м\n"
              "Цена - {price} грн\n"
              ).format(
                address=detail_data[1].get('address'),
                area=detail_data[1].get('area'),
                price=detail_data[1].get('price')
            ), parse_mode="HTML",
            reply_markup=management_keyboards.get_announcement_keyboard(int(callback_data.pk))
        )
    await callback.answer()


@router.callback_query(AnnouncementCallback.filter(F.key == "previous"))
async def announcement_next(callback: CallbackQuery, callback_data: MyCallback):
    ads_client = AdsApiClient(callback_data.pk)
    data = await ads_client.get_announcement_feed()
    if data:
        detail_data = data.get('data')
        await callback.message.answer_photo(
            photo=get_image(path=data.get('preview_image')),
            caption=
            _("Адрес - {address}\n"
              "Площадь - {area} кв.м\n"
              "Цена - {price} грн\n"
              ).format(
                address=detail_data[0].get('address'),
                area=detail_data[0].get('area'),
                price=detail_data[0].get('price')
            ), parse_mode="HTML",
            reply_markup=management_keyboards.get_announcement_keyboard(int(callback_data.pk))
        )
    await callback.answer()

# endregion feed
