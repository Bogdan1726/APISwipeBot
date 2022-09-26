from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from api_requests.user import UserApiClient
from keyboards import base_keyboard, registration_keyboard
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from settings.validators import validate_email, validate_name, validate_password
from aiogram import html
from settings.states import RegistrationStates

router = Router()


# region e-mail
@router.message(RegistrationStates.write_password1, F.text.lower() == __('назад'))
@router.message(F.text.lower() == __("регистрация"))
@router.message(RegistrationStates.start_registration)
async def register_email(message: Message, state: FSMContext) -> None:
    await message.answer(
        _("Введите e-mail:"),
        reply_markup=base_keyboard.get_cancel_keyboard()
    )
    await state.set_state(RegistrationStates.write_mail)


@router.message(RegistrationStates.register, F.text.lower() == __('редактировать email'))
async def register_edit_email(message: Message, state: FSMContext) -> None:
    await message.answer(
        _("Введите новый e-mail, или вернитесь обратно к данным"),
        reply_markup=registration_keyboard.get_back_register()
    )
    await state.set_state(RegistrationStates.edit_email)


@router.message(RegistrationStates.edit_email)
async def register_edit_email_check(message: Message, state: FSMContext) -> None:
    if message.text.lower() == _('вернутся к регистрации'):
        await register_last_name(message, state)
    else:
        email = message.text.lower()
        if validate_email(email) is False:
            await message.answer(
                _('Электронная почта - имеет неверный формат, ппопробуйте еще раз, или вернитесь обратно к данным'),
                reply_markup=registration_keyboard.get_back_register()
            )
        else:
            await state.update_data(email=email)
            await register_last_name(message, state)


# endregion e-mail

# region password 1

@router.message(RegistrationStates.write_first_name, F.text.lower() == __('назад'))
@router.message(RegistrationStates.write_password2, F.text.lower() == __('назад'))
@router.message(RegistrationStates.write_mail)
async def register_password1(message: Message, state: FSMContext) -> None:
    if message.text.lower() == __('назад'):
        await message.answer(
            _("Укажите пароль:"),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(RegistrationStates.write_password1)
    else:
        email = message.text.lower()
        if validate_email(email) is False:
            await message.answer(
                _('Электронная почта - имеет неверный формат, ппопробуйте еще раз'),
                reply_markup=base_keyboard.get_cancel_keyboard()
            )
            await state.set_state(RegistrationStates.write_mail)
        else:
            await state.update_data(email=email)
            await message.answer(
                _("Укажите пароль:"),
                reply_markup=base_keyboard.get_cancel_group_keyboard()
            )
            await state.set_state(RegistrationStates.write_password1)


@router.message(RegistrationStates.register, F.text.lower() == __('редактировать пароль'))
async def register_edit_password(message: Message, state: FSMContext) -> None:
    await message.answer(
        _("Введите новый пароль, или вернитесь обратно к данным"),
        reply_markup=registration_keyboard.get_back_register()
    )
    await state.set_state(RegistrationStates.edit_password)


@router.message(RegistrationStates.edit_password)
async def register_edit_password_check(message: Message, state: FSMContext) -> None:
    if message.text.lower() == __('вернутся к регистрации'):
        await register_last_name(message, state)
    else:
        password = message.text
        if validate_password(password) is False:
            await message.answer(
                _('Пароль слишком простой, попробуйте еще раз \n'
                  'Пароль должен: \n'
                  '- Содержать число \n'
                  '- Содержать символ верхнего и нижнего регистра \n'
                  '- Содержать минимум 8 символов\n'),
                reply_markup=registration_keyboard.get_back_register()
            )
        else:
            await state.update_data(password1=password)
            await register_last_name(message, state)


# endregion password 1

# region password 2
@router.message(RegistrationStates.write_password1)
async def register_password2(message: Message, state: FSMContext):
    password = message.text
    if validate_password(password) is False:
        await message.answer(
            _('Пароль слишком простой, попробуйте еще раз \n'
              'Пароль должен: \n'
              '- Содержать число \n'
              '- Содержать символ верхнего и нижнего регистра \n'
              '- Содержать минимум 8 символов\n'),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(RegistrationStates.write_password1)
    else:
        await state.update_data(password1=password)
        await message.answer(
            _("Повторите пароль:"),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(RegistrationStates.write_password2)


# endregion password 2

# region first_name
@router.message(RegistrationStates.write_last_name, F.text.casefold() == __('назад'))
@router.message(RegistrationStates.write_password2)
async def register_first_name(message: Message, state: FSMContext):
    if message.text.casefold() == __('назад'):
        await message.answer(
            _("Введите имя:"),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(RegistrationStates.write_first_name)
    else:
        data = await state.get_data()
        repeat_password = message.text
        password = data['password1']
        if repeat_password != password:
            await message.answer(
                _('Пароли не совпадают, попробуйте еще раз'),
                reply_markup=base_keyboard.get_cancel_group_keyboard()
            )
            await state.set_state(RegistrationStates.write_password2)
        else:
            await state.update_data(password2=message.text)
            await message.answer(
                _("Введите имя:"),
                reply_markup=base_keyboard.get_cancel_group_keyboard()
            )
            await state.set_state(RegistrationStates.write_first_name)


@router.message(RegistrationStates.register, F.text.lower() == __('редактировать имя'))
async def register_edit_first_name(message: Message, state: FSMContext) -> None:
    await message.answer(
        _("Введите имя заново, или вернитесь обратно к данным"),
        reply_markup=registration_keyboard.get_back_register()
    )
    await state.set_state(RegistrationStates.edit_first_name)


@router.message(RegistrationStates.edit_first_name)
async def register_first_name_check(message: Message, state: FSMContext) -> None:
    if message.text.lower() == __('вернутся к регистрации'):
        await register_last_name(message, state)
    else:
        first_name = message.text
        if validate_name(first_name) is False:
            await message.answer(
                _('Введенное имя некорректно, попробуйте еще раз, или вернитесь обратно к данным'),
                reply_markup=registration_keyboard.get_back_register()
            )
        else:
            await state.update_data(first_name=message.text)
            await register_last_name(message, state)


# endregion first_name

# region last_name
@router.message(RegistrationStates.write_first_name)
async def register_last_name(message: Message, state: FSMContext):
    first_name = message.text
    if validate_name(first_name) is False:
        await message.answer(
            _('Введенное имя некорректно, попробуйте еще раз'),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(RegistrationStates.write_first_name)
    else:
        await state.update_data(first_name=message.text)
        await message.answer(
            _("Введите фамилию:"),
            reply_markup=base_keyboard.get_cancel_group_keyboard()
        )
        await state.set_state(RegistrationStates.write_last_name)


@router.message(RegistrationStates.register, F.text.lower() == __('редактировать фамилию'))
async def register_edit_last_name(message: Message, state: FSMContext) -> None:
    await message.answer(
        _("Введите фамилию заново, или вернитесь обратно к данным"),
        reply_markup=registration_keyboard.get_back_register()
    )
    await state.set_state(RegistrationStates.edit_last_name)


@router.message(RegistrationStates.edit_last_name)
async def register_last_name_check(message: Message, state: FSMContext) -> None:
    if message.text.lower() == __('вернутся к регистрации'):
        await register_last_name(message, state)
    else:
        last_name = message.text
        if validate_name(last_name) is False:
            await message.answer(
                _('Введенная фамилия некорректна, попробуйте еще раз, или вернитесь обратно к данным'),
                reply_markup=registration_keyboard.get_back_register()
            )
        else:
            await state.update_data(last_name=last_name)
            await register_last_name(message, state)


# endregion last_name


# region data and send data
@router.message(F.text.lower() == __('вернутся к регистрации'))
@router.message(RegistrationStates.write_last_name)
@router.message(RegistrationStates.register_edit_data)
async def register_last_name(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == RegistrationStates.write_last_name:
        last_name = message.text
        if validate_name(last_name) is False:
            await message.answer(
                _('Введенная фамилия некорректна, попробуйте еще раз'),
                reply_markup=base_keyboard.get_cancel_group_keyboard()
            )
            await state.set_state(RegistrationStates.write_last_name)
        await state.update_data(last_name=last_name)
    data = await state.get_data()
    await message.answer(
        _('Ваши данные для регистрации \n'
          'E-mail: {email}\n'
          'Пароль: {password}\n'
          'Имя: {first_name}\n'
          'Фамилия: {last_name}\n'
          'Если все верно нажмите «Зарегистрироватся»\n'
          'Если вы хотите исправить данные, нажмите на кнопку с нужным вам полем\n'
          'Отменить регистрацию, нажмите «Отмена»').format(
            email=html.quote(data.get('email')),
            password=html.quote(data.get('password1')),
            first_name=html.quote(data.get('first_name')),
            last_name=html.quote(data.get('last_name')),

        ),
        reply_markup=registration_keyboard.get_register_keyboard()
    )
    await state.set_state(RegistrationStates.register)


@router.message(F.text.lower() == __("зарегистрироватся"))
async def registration(message: Message, state: FSMContext):
    validated_data = await state.get_data()
    user_client = UserApiClient(message.from_user.id)
    response = await user_client.register(validated_data)
    if response:
        await message.answer(
            _('Регистрация прошла успешно, письмо с подтверждением отправлено\n'
              'на почту {email}\n'
              'Перейдите по ссылке в письме для завершения регистрации').format(
                email=validated_data.get('email')
            ),
            reply_markup=base_keyboard.get_base_keyboard()
        )
        await state.clear()
    else:
        await message.answer(
            _('Ошибка регистрации, попробуйте еще\n'
              'Не забудьте убедится в правильности введенных данных'),
            reply_markup=registration_keyboard.get_register_keyboard()
        )

# endregion data and send data
