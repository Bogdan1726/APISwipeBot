import re
from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from api_requests.user import register
from keyboards import base_keyboard, registration_keyboard
from aiogram.fsm.state import StatesGroup, State

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
    write_mail = State()
    write_password1 = State()
    write_password2 = State()
    write_first_name = State()
    write_last_name = State()
    register = State()
    register_edit_data = State()


@router.message(Text(text="Регистрация"))
async def register_email(message: Message, state: FSMContext):
    await message.answer(
        "Введите e-mail:",
        reply_markup=base_keyboard.cancel
    )
    await state.set_state(RegistrationStates.write_mail)


@router.message(RegistrationStates.write_mail)
async def register_password1(message: Message, state: FSMContext):
    email = message.text.lower()
    if validate_email(email) is False:
        await message.answer(
            'Электронная почта - имеет неверный формат, пожалуйста, введите свой адрес электронной почты еще раз.'
        )
        await state.set_state(RegistrationStates.write_mail)
    else:
        await state.update_data(email=email)
        await message.answer(
            "Укажите пароль:",
        )
        await state.set_state(RegistrationStates.write_password1)


@router.message(RegistrationStates.write_password1)
async def register_password2(message: Message, state: FSMContext):
    password = message.text
    if validate_password(password) is False:
        await message.answer(
            f'Пароль слишком простой, попробуйте еще раз\n'
            f'Пароль должен:\n'
            f'- Содержать число\n'
            f'- Содержать символ верхнего и нижнего регистра\n'
            f'- Содержать минимум 8 символов'
        )
        await state.set_state(RegistrationStates.write_password1)
    else:
        await state.update_data(password1=message.text)
        await message.answer(
            "Повторите пароль:",
        )
        await state.set_state(RegistrationStates.write_password2)


@router.message(RegistrationStates.write_password2)
async def register_first_name(message: Message, state: FSMContext):
    data = await state.get_data()
    repeat_password = message.text
    password = data['password1']
    if repeat_password != password:
        await message.answer(
            'Пароли не совпадают.'
        )
        await state.set_state(RegistrationStates.write_password2)
    else:
        await state.update_data(password2=message.text)
        await message.answer(
            "Введите имя:",
        )
        await state.set_state(RegistrationStates.write_first_name)


@router.message(RegistrationStates.write_first_name)
async def register_last_name(message: Message, state: FSMContext):
    first_name = message.text
    if validate_name(first_name) is False:
        await message.answer(
            'Введенное имя некорректно'
        )
        await state.set_state(RegistrationStates.write_first_name)
    else:
        await state.update_data(first_name=message.text)
        await message.answer(
            "Введите фамилию:",
        )
        await state.set_state(RegistrationStates.write_last_name)


@router.message(Text(text="Назад"))
@router.message(RegistrationStates.write_last_name)
async def register_last_name(message: Message, state: FSMContext):
    last_name = message.text
    if validate_name(last_name) is False:
        await message.answer(
            'Введенная фамилия некорректна'
        )
        await state.set_state(RegistrationStates.write_last_name)
    else:
        await state.update_data(last_name=message.text)
        data = await state.get_data()
        await message.answer(
            f'Ваши данные для регистрации \n'
            f'E-mail: {data.get("email")}\n'
            f'Пароль: {data.get("password1")}\n'
            f'Имя: {data.get("first_name")}\n'
            f'Фамилия: {data.get("last_name")}\n'
            f'Если все верно нажмите «Зарегистрироватся»\n'
            f'Если вы хотите исправить данные, нажмите «Изменить данные»\n'
            f'Отменить регистрацию, нажмите «Отмена»',
            reply_markup=registration_keyboard.reg_keyboard.as_markup(resize_keyboard=True)
        )
        await state.set_state(RegistrationStates.register)


@router.message(Text(text="Зарегистрироватся"))
async def registration(message: Message, state: FSMContext):
    validated_data = await state.get_data()
    if await register(validated_data, message.from_user.id) is True:
        await message.answer(
            f'Регистрация прошла успешно, письмо с подтверждением отправлено '
            f'на почту {validated_data.get("email")}\n'
            f'Перейдите по ссылке в письме для завершения регистрации',
            reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True)
        )
        await state.clear()
    else:
        await message.answer(
            f'Ошибка регистрации, попробуйте еще\n'
            f'Не забудьте убедится в правильности введенных данных',
            reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True)
        )


@router.message(Text(text="Изменить данные"))
async def register_edit_data(message: Message, state: FSMContext):
    data = await state.get_data()
    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    await message.answer(
        f'Чтобы изменить данные, скопируйте шаблон ниже и отредактирував нужные поля пришлите его сообщением\n\n'
        f'E-mail: {email}\n'
        f'Пароль: {password1}\n'
        f'Повторите пароль: {password2}\n'
        f'Имя: {first_name}\n'
        f'Фамилия: {last_name}\n\n'
        f'Передумали!? Нажмите кнопку «Назад»\n'
        f'Отменить регистрацию, нажмите «Отмена»',
        reply_markup=registration_keyboard.reg_keyboard_edit
    )
    await state.set_state(RegistrationStates.register_edit_data)


@router.message(RegistrationStates.register_edit_data)
async def register_edit_data_done():
    pass
