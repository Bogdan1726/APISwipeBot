import re

from aiogram import types, Router
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import base_keyboard
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
        await state.update_data(mail=email)
        await message.answer(
            "Введите пароль:",
        )
        await state.set_state(RegistrationStates.write_password1)


@router.message(RegistrationStates.write_password1)
async def register_password2(message: Message, state: FSMContext):
    password = message.text
    if validate_password(password) is False:
        await message.answer(
            'Пароль слишком простой, попробуйте еще раз.'
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
            f'Ваши данные{data}'
        )
        await state.clear()
