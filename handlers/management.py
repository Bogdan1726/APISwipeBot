from aiogram import Router, F
from aiogram.types import Message
from api_requests.user import UserApiClient
from database.requests import is_authenticated
from keyboards import base_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram import html
from aiogram.utils.i18n import lazy_gettext as __
from settings.states import ProfileStates, BaseStates
from settings.validators import validate_email, validate_name, validate_phone

router = Router()


# region profile


@router.message(F.text.lower() == __("профиль"))
@router.message(F.text.lower() == __("назад в профиль"))
async def user_profile(message: Message, state: FSMContext):
    user = message.from_user.id
    user_client = UserApiClient(user)
    if is_authenticated(user):
        data = await user_client.profile()
        if data:
            await message.answer(
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


@router.message(F.text.casefold() == __("отменить редактирование"))
@router.message(F.text.lower() == __("редактировать профиль"))
@router.message(ProfileStates.profile)
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
        await user_client.profile_update(data)


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

# endregion profile
