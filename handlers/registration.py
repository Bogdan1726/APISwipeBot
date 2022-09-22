import re
from aiogram import Router, F
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from api_requests.user import register
from keyboards import base_keyboard, registration_keyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from aiogram import html

router = Router()


# region validators
def validate_email(email: str) -> bool:
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
    if re.match(pattern, email) is None:
        return False
    else:
        return True


def validate_password(password: str) -> bool:
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    if pattern_password.match(password):
        return True
    else:
        return False


def validate_name(value: str) -> bool:
    if value.isalpha() and value.istitle() and 2 <= len(value) <= 24:
        return True
    return False


# endregion validators

class RegistrationStates(StatesGroup):
    start_registration = State()
    write_mail = State()
    write_password1 = State()
    write_password2 = State()
    write_first_name = State()
    write_last_name = State()
    register = State()
    register_edit_data = State()


@router.message(RegistrationStates.register, F.text.casefold() == 'редактировать email')
@router.message(RegistrationStates.write_password1, F.text.casefold() == 'назад')
@router.message(Text(text="Регистрация"))
@router.message(RegistrationStates.start_registration)
async def register_email(message: Message, state: FSMContext):
    if message.text.casefold() == 'редактировать email':
        await state.set_state(RegistrationStates.write_last_name)
        await message.answer(
            _("Введите e-mail:"),
            reply_markup=registration_keyboard.to_reg_data
        )
    else:
        await state.set_state(RegistrationStates.write_mail)
        await message.answer(
            _("Введите e-mail:"),
            reply_markup=base_keyboard.cancel_keyboard
        )


@router.message(RegistrationStates.write_password2, F.text.casefold() == 'назад')
@router.message(RegistrationStates.write_mail)
async def register_password1(message: Message, state: FSMContext):
    if message.text.casefold() == 'назад':
        await message.answer(
            _("Укажите пароль:"),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_password1)
    else:
        email = message.text.lower()
        if validate_email(email) is False:
            await message.answer(
                _('Электронная почта - имеет неверный формат, пожалуйста, введите свой адрес электронной почты еще раз'),
                reply_markup=base_keyboard.cancel
            )
            await state.set_state(RegistrationStates.write_mail)
        else:
            await state.update_data(email=email)
            await message.answer(
                _("Укажите пароль:"),
                reply_markup=base_keyboard.cancel
            )
            await state.set_state(RegistrationStates.write_password1)


@router.message(RegistrationStates.write_first_name, F.text.casefold() == 'назад')
@router.message(RegistrationStates.write_password1)
async def register_password2(message: Message, state: FSMContext):
    password = message.text
    if validate_password(password) is False:
        await message.answer(
            _('Пароль слишком простой, попробуйте еще раз \n'
              'Пароль должен: \n'
              '- Содержать число \n'
              '- Содержать символ верхнего и нижнего регистра \n'
              '- Содержать минимум 8 символов'),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_password1)
    else:
        await state.update_data(password1=message.text)
        await message.answer(
            _("Повторите пароль:"),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_password2)


@router.message(RegistrationStates.write_last_name, F.text.casefold() == 'назад')
@router.message(RegistrationStates.write_password2)
async def register_first_name(message: Message, state: FSMContext):
    data = await state.get_data()
    repeat_password = message.text
    password = data['password1']
    if repeat_password != password:
        await message.answer(
            _('Пароли не совпадают'),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_password2)
    else:
        await state.update_data(password2=message.text)
        await message.answer(
            _("Введите имя:"),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_first_name)


@router.message(RegistrationStates.register, F.text.casefold() == 'назад')
@router.message(RegistrationStates.write_first_name)
async def register_last_name(message: Message, state: FSMContext):
    first_name = message.text
    if validate_name(first_name) is False:
        await message.answer(
            _('Введенное имя некорректно'),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_first_name)
    else:
        await state.update_data(first_name=message.text)
        await message.answer(
            _("Введите фамилию:"),
            reply_markup=base_keyboard.cancel
        )
        await state.set_state(RegistrationStates.write_last_name)


@router.message(F.text.casefold() == 'вернутся к регистрации')
@router.message(RegistrationStates.write_last_name)
async def register_last_name(message: Message, state: FSMContext):
    if message.text.casefold() == 'вернутся к регистрации':
        data = await state.get_data()
        await message.answer(
            _('Ваши данные для регистрации \n'
              'E-mail: {email}\n'
              'Пароль: {password}\n'
              'Имя: {first_name}\n'
              'Фамилия: {last_name}\n'
              'Если все верно нажмите «Зарегистрироватся»\n'
              'Если вы хотите исправить данные, нажмите «Изменить данные»\n'
              'Отменить регистрацию, нажмите «Отмена»').format(
                email=html.quote(data.get('email')),
                password=html.quote(data.get('password1')),
                first_name=html.quote(data.get('first_name')),
                last_name=html.quote(data.get('last_name')),

            ),
            reply_markup=registration_keyboard.reg_keyboard
        )
        await state.set_state(RegistrationStates.register)
    else:
        last_name = message.text
        if validate_name(last_name) is False:
            await message.answer(
                _('Введенная фамилия некорректна'),
                reply_markup=base_keyboard.cancel
            )
            await state.set_state(RegistrationStates.write_last_name)
        else:
            await state.update_data(last_name=message.text)
            data = await state.get_data()
            await message.answer(
                _('Ваши данные для регистрации \n'
                  'E-mail: {email}\n'
                  'Пароль: {password}\n'
                  'Имя: {first_name}\n'
                  'Фамилия: {last_name}\n'
                  'Если все верно нажмите «Зарегистрироватся»\n'
                  'Если вы хотите исправить данные, нажмите «Изменить данные»\n'
                  'Отменить регистрацию, нажмите «Отмена»').format(
                    email=html.quote(data.get('email')),
                    password=html.quote(data.get('password1')),
                    first_name=html.quote(data.get('first_name')),
                    last_name=html.quote(data.get('last_name')),

                ),
                reply_markup=registration_keyboard.reg_keyboard
            )
            await state.set_state(RegistrationStates.register)


@router.message(Text(text="Зарегистрироватся"))
async def registration(message: Message, state: FSMContext):
    validated_data = await state.get_data()
    if await register(validated_data) is True:
        await message.answer(
            _('Регистрация прошла успешно, письмо с подтверждением отправлено\n'
              'на почту {email}\n'
              'Перейдите по ссылке в письме для завершения регистрации').format(
                email=validated_data.get('email')
            ),
            reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True)
        )
        await state.clear()
    else:
        await message.answer(
            _('Ошибка регистрации, попробуйте еще\n'
              'Не забудьте убедится в правильности введенных данных'),
            reply_markup=registration_keyboard.reg_keyboard
        )


@router.message(RegistrationStates.register_edit_data)
async def register_edit_data_done():
    pass
