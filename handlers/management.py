import os
from aiogram import Router, F, Bot
from aiogram.types import Message, URLInputFile, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from yarl import URL
from api_requests.user import UserApiClient, AdsApiClient
from database.requests import is_authenticated
from keyboards import base_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram import html
from aiogram.utils.i18n import lazy_gettext as __
from keyboards.management_keyboards import MyCallback
from settings.config import HOST, DEFAULT_IMAGE
from settings.states import ProfileStates, BaseStates, AuthenticationStates, AnnouncementStates, AdsEditStates
from settings.validators import (
    validate_email, validate_name, validate_phone, validate_image, validate_purpose,
    validate_address, validate_house, validate_area, validate_kitchen, validate_room, validate_condition,
    validate_description, validate_price, parse_ads_data, validate_image_ads
)

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

@router.message(AuthenticationStates.main_menu, F.text.lower() == __("профиль"))
@router.message(ProfileStates.edit_profile, F.text.lower() == __("назад в профиль"))
@router.message(ProfileStates.ads, F.text.lower() == __("назад в профиль"))
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
            await state.set_state(BaseStates.auth)
    else:
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.get_base_keyboard())
        await state.set_state(BaseStates.auth)


@router.message(ProfileStates.profile, F.text.lower() == __("редактировать профиль"))
@router.message(ProfileStates.email, F.text.lower() == __("отменить редактирование"))
@router.message(ProfileStates.first_name, F.text.lower() == __("отменить редактирование"))
@router.message(ProfileStates.last_name, F.text.lower() == __("отменить редактирование"))
@router.message(ProfileStates.phone, F.text.lower() == __("отменить редактирование"))
@router.message(ProfileStates.photo, F.text.lower() == __("отменить редактирование"))
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
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.get_base_keyboard())
        await state.set_state(BaseStates.auth)


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
@router.message(ProfileStates.add_ads, F.text.lower() == __('вернутся к объявлениям'))
@router.message(ProfileStates.profile, F.text.lower() == __("мои обьявления"))
@router.message(ProfileStates.ads, F.text.lower() == __('назад в мои обьявления'))
@router.message(AdsEditStates.edit, F.text.lower() == __('назад в мои обьявления'))
@router.message(AdsEditStates.edit_ads_fields, F.text.lower() == __('назад в мои обьявления'))
async def user_ads(message: Message, state: FSMContext):
    user = message.from_user.id
    user_client = UserApiClient(user)
    if is_authenticated(user):
        data = await user_client.user_ads()
        if data:
            await message.answer("Вот список ваших объявления", reply_markup=ReplyKeyboardRemove())
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
            await message.answer(
                text=_('Чтобы отредактировать объявление, нажмите кнопку рядом с нужным вам объявлением'),
                reply_markup=management_keyboards.get_my_ads_keyboards()
            )
            await state.set_state(ProfileStates.ads)
        else:
            await message.answer(
                _('У вас нет ни одного объявления!'),
                reply_markup=management_keyboards.get_profile_cancel()
            )
        await state.set_state(ProfileStates.ads)
    else:
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.get_base_keyboard())
        await state.set_state(BaseStates.auth)


# endregion my ads


# region edit ads


@router.callback_query(MyCallback.filter(F.key == "edit_ads"))
async def edit_ads(callback: CallbackQuery, callback_data: MyCallback, state: FSMContext):
    await state.update_data(pk=callback_data.pk)
    await state.set_state(AdsEditStates.edit)
    await ads_edit(callback.message, state)
    await callback.answer()


@router.message(AdsEditStates.address, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.description, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.price, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.area, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.area_kitchen, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.layout, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.founding_document, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.rooms, F.text.lower() == __('отменить редактирование'))
@router.message(AdsEditStates.condition, F.text.lower() == __('отменить редактирование'))
async def ads_edit(message: Message, state: FSMContext) -> None:
    await message.answer(
        _('Для изменения данных нажмите кнопку c нужным для вас полем'),
        reply_markup=management_keyboards.get_profile_edit_ads()
    )
    await state.set_state(AdsEditStates.edit_ads_fields)


@router.message(AdsEditStates.edit_ads_fields)
async def select_field_ads(message: Message, state: FSMContext):
    text = message.text
    if text.lower() == __("адрес"):
        await message.answer(
            _("Введите адрес:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(AdsEditStates.address)
    elif text.lower() == __("описание"):
        await message.answer(
            _("Введите описание:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(AdsEditStates.description)
    elif text.lower() == __("стоимость"):
        await message.answer(
            _("Введите стоимость:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(AdsEditStates.price)
    elif text.lower() == __("общая площадь"):
        await message.answer(
            _("Введите общую площадь:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(AdsEditStates.area)
    elif text.lower() == __("площадь кухни"):
        await message.answer(
            _("Введите площадь кухни:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(AdsEditStates.area_kitchen)
    elif text.lower() == __("планировка"):
        await message.answer(
            _("Выберите планировку:"),
            reply_markup=management_keyboards.edit_ads_layout_keyboard()
        )
        await state.set_state(AdsEditStates.layout)
    elif text.lower() == __("вид права"):
        await message.answer(
            _("Выберите вид права:"),
            reply_markup=management_keyboards.edit_ads_founding_document_keyboard()
        )
        await state.set_state(AdsEditStates.founding_document)

    elif text.lower() == __("количество комнат"):
        await message.answer(
            _("Введите Количество комнат:"),
            reply_markup=management_keyboards.get_cancel_keyboard()
        )
        await state.set_state(AdsEditStates.rooms)
    elif text.lower() == __("жилое состояние"):
        await message.answer(
            _("Выберите жилое состояние:"),
            reply_markup=management_keyboards.edit_ads_condition_keyboard()
        )
        await state.set_state(AdsEditStates.area)
    else:
        await message.answer(
            _('Нет такой команды, попробуйте еще раз!')
        )
        await state.set_state(ProfileStates.profile)



# endregion edit ads


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
            reply_markup=management_keyboards.add_ads_back_keyboard()
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
                    reply_markup=management_keyboards.add_ads_back_keyboard()
                )
                await state.set_state(ProfileStates.add_ads_purpose)


@router.message(ProfileStates.add_ads_house)
async def add_ads_house(message: Message, state: FSMContext):
    house = message.text
    if validate_house(house) is False:
        await message.answer(
            _('Выбраного значения нет среди допустимых вариантов, попробуйте еще из доступных ниже вариантов\n'),
            reply_markup=management_keyboards.add_ads_house_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_house)
    else:
        await state.update_data(house=house)
        await message.answer(
            _('Укажите адрес'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_purpose)


@router.message(ProfileStates.add_ads_area, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_purpose)
async def add_ads_address(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Укажите площадь'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_address)
    else:
        address = message.text
        if validate_address(address) is False:
            await message.answer(
                _('Адрес - имеет неверный формат, попробуйте еще раз\n'
                  'Ниже приведен пример правильного формата ввода\n\n'
                  'р-н Центральный, ул. Темерязева 7'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_purpose)
        else:
            await state.update_data(address=address)
            await message.answer(
                _('Укажите площадь'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_address)


@router.message(ProfileStates.add_ads_area_kitchen, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_address)
async def add_ads_area(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Укажите площадь кухни'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_area)
    else:
        area = message.text
        if validate_area(area) is False:
            await message.answer(
                _('Площадь - имеет неверный формат, попробуйте еще раз\n'
                  'Ниже приведен пример правильного формата ввода\n\n'
                  '75'
                  ),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_address)
        else:
            await state.update_data(area=area)
            await message.answer(
                _('Укажите площадь кухни'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_area)


@router.message(ProfileStates.add_ads_room, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_area)
async def add_ads_area_kitchen(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Укажите количество комнат'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_area_kitchen)
    else:
        data = await state.get_data()
        area_kitchen = message.text
        if validate_kitchen(data.get('area'), area_kitchen) is False:
            await message.answer(
                _('Площадь кухни - имеет неверный формат\n'
                  'Площадь кухни – не может быть больше общей площади, попробуйте еще раз'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_area)
        else:
            await state.update_data(area_kitchen=area_kitchen)
            await message.answer(
                _('Укажите количество комнат'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_area_kitchen)


@router.message(ProfileStates.add_ads_condition, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_area_kitchen)
async def add_ads_room(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Выберите жилое состояние'),
            reply_markup=management_keyboards.add_ads_condition_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_room)
    else:
        room = message.text
        if validate_room(room) is False:
            await message.answer(
                _('Количество комнат – должно быть от 1-ой до 10-ти \n'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_area_kitchen)
        else:
            await state.update_data(room=room)
            await message.answer(
                _('Выберите жилое состояние'),
                reply_markup=management_keyboards.add_ads_condition_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_room)


@router.message(ProfileStates.add_ads_description, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_room)
async def add_ads_condition(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Добавьте описание (мин.длина 20 символов)'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_condition)
    else:
        condition = message.text
        if validate_condition(condition) is False:
            await message.answer(
                _('Выбраного значения нет среди допустимых вариантов, попробуйте еще из доступных ниже вариантов\n'),
                reply_markup=management_keyboards.add_ads_condition_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_room)
        else:
            await state.update_data(condition=condition)
            await message.answer(
                _('Добавьте описание (мин.длина 20 символов)'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_condition)


@router.message(ProfileStates.add_ads_price, F.text.lower() == __('назад'))
@router.message(ProfileStates.add_ads_condition)
async def add_ads_description(message: Message, state: FSMContext):
    if message.text.lower() == __('назад'):
        await message.answer(
            _('Установите цену'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_description)
    else:
        description = message.text
        if validate_description(description) is False:
            await message.answer(
                _('Описание - имеет неверный формат\n'
                  'Описание - должно состоять минимум из 20 символов кириллицы'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_condition)
        else:
            await state.update_data(description=description)
            await message.answer(
                _('Установите цену'),
                reply_markup=management_keyboards.add_ads_back_keyboard()
            )
            await state.set_state(ProfileStates.add_ads_description)


@router.message(ProfileStates.add_ads_description)
async def edit_photo(message: Message, state: FSMContext, bot: Bot):
    price = message.text.replace(' ', '')
    if validate_price(price) is False:
        await message.answer(
            _('Цена - имеет неверный формат\n'
              'Диапазон доступной цены – от 0 грн. до 100 000 000 грн.'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_description)
    else:
        await state.update_data(price=price)
        await message.answer(
            _("Прикрепите одну фотографию в сообщении\n"
              "Рекомендуемый размер: (800x800)\n"
              "И не более 20 мегабайт"),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )
        await state.set_state(ProfileStates.add_ads_price)


@router.message(ProfileStates.add_ads_price)
async def add_ads_description(message: Message, state: FSMContext, bot: Bot):
    try:
        photo = message.photo[-1]
        if validate_image_ads(photo) is False:
            await message.answer(
                _('Фото превышает рекомендуемый размер')
            )
            await state.set_state(ProfileStates.add_ads_price)
        else:
            file = await bot.get_file(photo.file_id)
            filename, file_extension = os.path.splitext(file.file_path)
            src = 'files/ads/' + file.file_id + file_extension
            await bot.download_file(file_path=file.file_path, destination=src)
            await state.update_data(ads_image_src=src)
            data = await state.get_data()
            image = FSInputFile(data.get('ads_image_src'))
            await message.answer_photo(
                photo=image,
                caption=
                _('Адрес: {address}\n'
                  'Назначение: {purpose}\n'
                  'Жилой комплекс: {house}\n'
                  'Жилое состояние: {condition}\n'
                  'Общая площадь: {area} м2\n'
                  'Площадь кухни: {area_kitchen} м2\n'
                  'Количество комнат: {room} \n'
                  'Описание: {description}\n'
                  'Цена: {price} - грн\n'
                  'Если все верно нажмите «Добавить»\n'
                  'Если вы хотите исправить данные, нажимайте «Назад»\n'
                  ).format(
                    address=data.get('address'),
                    house=data.get('house') if data.get(
                        'house') else 'Вы выбрали назначение которое не требует выбора ЖК',
                    purpose=data.get('purpose'),
                    condition=data.get('condition'),
                    area=data.get('area'),
                    description=data.get('description'),
                    area_kitchen=data.get('area_kitchen'),
                    price=data.get('price'),
                    room=data.get('room')),
                reply_markup=management_keyboards.add_ads_finish()
            )
            await state.set_state(ProfileStates.add_ads_data)
    except TypeError:
        await message.answer(
            _('Недопустимый формат фотографии'),
            reply_markup=management_keyboards.add_ads_back_keyboard()
        )


@router.message(ProfileStates.add_ads_data, F.text.lower() == __('добавить'))
async def add_ads(message: Message, state: FSMContext):
    data = await state.get_data()
    validated_data = parse_ads_data(data)
    ads_client = AdsApiClient(message.from_user.id)
    if await ads_client.create_ads(validated_data):
        await message.answer(
            _('Объявления успешно добавлено'),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        await user_ads(message, state)
    else:
        await message.answer(
            _('При попытке добавить объявление произошла ошибка, попробуйте еще'),
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()
        await user_ads(message, state)

# endregion add ads
