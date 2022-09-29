import os
from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.types import Message, URLInputFile, CallbackQuery
from babel.core import Locale
from yarl import URL
from api_requests.user import UserApiClient
from database.requests import is_authenticated
from keyboards import base_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram import html
from aiogram.utils.i18n import lazy_gettext as __

from keyboards.management_keyboards import MyCallback
from settings.config import HOST, DEFAULT_IMAGE
from settings.states import ProfileStates, BaseStates
from settings.validators import validate_email, validate_name, validate_phone, validate_image, validate_purpose, \
    validate_address

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


# region profile

@router.message(F.text.lower() == __("профиль"))
@router.message(F.text.lower() == __("назад в профиль"))
async def user_profile(message: Message, state: FSMContext):
    user = message.from_user.id
    user_client = UserApiClient(user)
    if is_authenticated(user):
        data = await user_client.profile()
        if data:
            await message.answer_photo(
                photo=get_image(data.get('profile_image')),
                caption=
                _('Имя: {first_name}\n'
                  'Фамилия: {last_name}\n'
                  'Телефон: {phone}\n'
                  'E-mail: {email}').format(
                    first_name=html.quote(data.get('first_name')),
                    last_name=html.quote(data.get('last_name')),
                    phone=html.quote(data.get('phone')) if data.get('phone') else "Нет даных",
                    email=html.quote(data.get('email')),
                ), parse_mode="HTML",
                reply_markup=management_keyboards.get_profile_keyboard()
            )
            await state.update_data(data)
            await state.set_state(ProfileStates.profile)
        else:
            await message.answer(
                _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
                reply_markup=base_keyboard.get_base_keyboard())
            await state.set_state(BaseStates.start)
    else:
        await state.set_state(BaseStates.language)


@router.message(F.text.lower() == __("редактировать профиль"))
@router.message(F.text.lower() == __("отменить редактирование"))
async def user_profile_edit(message: Message, state: FSMContext):
    user = message.from_user.id
    if is_authenticated(user):
        await message.answer(
            _('Для изменения данных нажмите кнопку c нужным для вас полем'),
            parse_mode="HTML",
            reply_markup=management_keyboards.get_profile_edit_keyboard()
        ),
        await state.set_state(ProfileStates.edit_profile)
    else:
        await state.set_state(BaseStates.language)


@router.message(ProfileStates.edit_profile)
async def select_field(message: Message, state: FSMContext):
    text = message.text
    if text.lower() == __("редактировать email"):
        await message.answer(
            _("Введите e-mail:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.email)
    elif text.lower() == __("редактировать телефон"):
        await message.answer(
            _("Введите телефон:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.phone)
    elif text.lower() == __("редактировать имя"):
        await message.answer(
            _("Введите имя:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.first_name)
    elif text.lower() == __("редактировать фамилию"):
        await message.answer(
            _("Введите фамилию:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.last_name)
    elif text.lower() == __("установить новое фото профиля"):
        await message.answer(
            _("Прикрепите новое фото в сообщении\n"
              "Рекомендуемый размер: (300x300)\n"
              "И не более 20 мегабайт"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.photo)
    else:
        await message.answer(
            _('Я не знаю такой команды, попробуйте еще раз!')
        )
        await state.set_state(ProfileStates.profile)


@router.message(ProfileStates.email)
async def edit_email(message: Message, state: FSMContext):
    email = message.text
    if validate_email(email) is False:
        await message.answer(
            _('Электронная почта - имеет неверный формат, пожалуйста, введите адрес электронной почты еще раз'),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.email)
    else:
        await state.update_data(email=email)
        data = await state.get_data()
        user_client = UserApiClient(message.from_user.id)
        if await user_client.profile_update(data):
            await message.answer(
                _('Электронная почта успешно изменена'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)
        else:
            await message.answer(
                _('Возникла ошибка при попытке изменить электронную почту'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)


@router.message(ProfileStates.phone)
async def edit_phone(message: Message, state: FSMContext):
    phone = message.text
    if validate_phone(phone) is False:
        await message.answer(
            _('Номер телефона - имеет неверный формат, введите телефон еще раз'),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.phone)
    else:
        await state.update_data(phone=phone)
        data = await state.get_data()
        user_client = UserApiClient(message.from_user.id)
        if await user_client.profile_update(data):
            await message.answer(
                _('Номер телефона успешно изменен'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)
        else:
            await message.answer(
                _('Возникла ошибка при попытке изменить номер телефона'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)


@router.message(ProfileStates.first_name)
async def edit_first_name(message: Message, state: FSMContext):
    first_name = message.text
    if validate_name(first_name) is False:
        await message.answer(
            _('Имя  - имеет неверный формат, введите имя еще раз'),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.first_name)
    else:
        await state.update_data(first_name=first_name)
        data = await state.get_data()
        user_client = UserApiClient(message.from_user.id)
        if await user_client.profile_update(data):
            await message.answer(
                _('Имя успешно изменено'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)
        else:
            await message.answer(
                _('Возникла ошибка при попытке изменить имя'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)


@router.message(ProfileStates.last_name)
async def edit_last_name(message: Message, state: FSMContext):
    last_name = message.text
    if validate_name(last_name) is False:
        await message.answer(
            _('Фамилия  - имеет неверный формат, введите фимилию еще раз'),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(ProfileStates.last_name)
    else:
        await state.update_data(last_name=last_name)
        data = await state.get_data()
        user_client = UserApiClient(message.from_user.id)
        if await user_client.profile_update(data):
            await message.answer(
                _('Фамилия успешно изменена'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)
        else:
            await message.answer(
                _('Возникла ошибка при попытке изменить фамилию'),
                reply_markup=management_keyboards.get_profile_edit_keyboard()
            )
            await state.set_state(ProfileStates.edit_profile)


@router.message(ProfileStates.photo)
async def edit_photo(message: Message, state: FSMContext, bot: Bot):
    try:
        photo = message.photo[-1]
        if validate_image(photo) is False:
            await message.answer(
                _('Фото превышает рекомендуемый размер')
            )
        else:
            file = await bot.get_file(photo.file_id)
            filename, file_extension = os.path.splitext(file.file_path)
            src = 'files/' + file.file_id + file_extension
            await bot.download_file(file_path=file.file_path, destination=src)
            await state.update_data(profile_image_src=src)
            data = await state.get_data()
            user_client = UserApiClient(message.from_user.id)
            if await user_client.profile_update(data):
                await message.answer(
                    _('Фото профиля успешно изменено'),
                    reply_markup=management_keyboards.get_profile_edit_keyboard()
                )
                await state.set_state(ProfileStates.edit_profile)
            else:
                await message.answer(
                    _('Возникла ошибка при попытке изменить фото профиля'),
                    reply_markup=management_keyboards.get_profile_edit_keyboard()
                )
                await state.set_state(ProfileStates.edit_profile)
    except TypeError:
        await message.answer(
            _('Недопустимый формат фотографии'),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )


# endregion profile


# region my ads
@router.message(F.text.lower() == __('вернутся к объявлениям'))
@router.message(F.text.lower() == __("мои обьявления"))
@router.message(F.text.lower() == __('назад в мои обьявления'))
async def user_ads(message: Message, state: FSMContext):
    user = message.from_user.id
    user_client = UserApiClient(user)
    if is_authenticated(user):
        data = await user_client.user_ads()
        if data:
            await message.answer(
                text=_('Чтобы отредактировать объявление, нажмите кнопку рядом с нужным вам объявлением'),
                reply_markup=management_keyboards.get_my_ads_keyboards()
            )
            await state.set_state(ProfileStates.ads)
            for ads in data:
                await message.answer_photo(
                    photo=get_image(path=ads.get('preview_image')),
                    caption=
                    _("{purpose}\n"
                      "Адрес - {address}\n"
                      "Площадь - {area} кв.м\n"
                      "Планировка - {layout}\n"
                      "Количество комнат - {rooms}\n"
                      "Жилое состояние - {condition}\n"
                      "Цена - {price} грн\n"
                      "{description}\n").format(
                        address=ads.get('address'),
                        area=ads.get('area'),
                        rooms=ads.get('rooms'),
                        price=ads.get('price'),
                        purpose=html.bold(ads.get('purpose')),
                        layout=ads.get('layout'),
                        condition=ads.get('condition'),
                        description=html.italic(ads.get('description'))
                    ), parse_mode="HTML",
                    reply_markup=management_keyboards.get_edit_ads_keyboard(pk=ads.get('id'))
                )
        else:
            await message.answer(
                _('У вас нет ни одного объявления!'),
                reply_markup=management_keyboards.get_profile_cancel()
            )
        await state.set_state(ProfileStates.ads)
    else:
        await state.set_state(BaseStates.language)


@router.callback_query(MyCallback.filter(F.key == "edit_ads"))
async def edit_ads(callback: CallbackQuery, callback_data: MyCallback):
    await callback.message.answer(
        _('Для изменения данных нажмите кнопку c нужным для вас полем'),
        reply_markup=management_keyboards.get_profile_edit_ads()
    )


@router.message(F.text.lower() == 'адрес')
async def edit_ads_address(message: Message):
    await message.answer(
        f'{message.from_user}'
    )


# endregion my ads


# region add ads
@router.message(ProfileStates.add_ads_purpose, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_house, F.text.lower() == __('назад'))
@router.message(ProfileStates.ads, F.text.lower() == __("добавить объявление"))
@router.message(ProfileStates.ads)
async def add_ads_start(message: Message, state: FSMContext):
    await message.answer(
        _('Выберите назначение объявления из доступных ниже вариантов\n'),
        reply_markup=management_keyboards.add_ads_purpose_keyboard()
    )
    await state.set_state(ProfileStates.add_ads)


@router.message(ProfileStates.add_ads_address, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads)
async def add_ads_purpose(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Укажите адрес'),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_purpose)
    else:
        purpose = message.text
        if validate_purpose(purpose) is False:
            await message.answer(
                _('Выбраного значения нет среди допустимых вариантов, попробуйте еще из доступных ниже вариантов\n'),
                reply_markup=management_keyboards.add_ads_purpose_keyboard()
            )
            await state.set_state(ProfileStates.add_ads)
        else:
            await state.update_data(purpose=purpose)
            if purpose == 'Квартира':
                await message.answer(
                    _('Выберите ЖК из доступных ниже вариантов'),
                    reply_markup=management_keyboards.add_ads_house_keyboard()
                )
                await state.set_state(ProfileStates.add_ads_house)
            else:
                await message.answer(
                    _('Укажите адрес'),
                    reply_markup=base_keyboard.get_cancel_group_keyboard()
                )
                await state.set_state(ProfileStates.add_ads_purpose)


@router.message(ProfileStates.add_ads_purpose)
async def add_ads_address(message: Message, state: FSMContext):
    address = message.text
    if validate_address(address) is False:
        await message.answer(
            _('Адрес - имеет неверный формат, ппопробуйте еще раз'),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_purpose)
    else:
        await message.answer(
            _('Укажите площадь'),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_address)

# endregion add ads
