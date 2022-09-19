from aiogram import types, Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command, Text
from aiogram.types import Message
from api_requests.user import login
from keyboards import base_keyboard, authentication_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class AuthenticationStates(StatesGroup):
    write_mail = State()
    write_password = State()
    auth = State()


@router.message(Text(text="Вход"))
async def login_email(message: Message, state: FSMContext):
    await message.answer(
        "Введите e-mail:",
        reply_markup=base_keyboard.cancel
    )
    await state.set_state(AuthenticationStates.write_mail)


@router.message(AuthenticationStates.write_mail)
async def login_password(message: Message, state: FSMContext):
    await state.update_data(email=message.text.lower())
    await message.answer(
        "Введите пароль:",
        reply_markup=base_keyboard.cancel
    )
    await state.set_state(AuthenticationStates.write_password)


@router.message(AuthenticationStates.write_password)
async def authentication(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await message.answer(
        f'Ваши данные для входа \n'
        f'E-mail: {data.get("email")}\n'
        f'Пароль: {data.get("password")}\n'
        f'Если все верно нажмите кнопку «Авторизоватся»\n'
        f'В противном случае нажмите «Отмена» и повторите попытку',
        reply_markup=base_keyboard.auth
    )
    await state.set_state(AuthenticationStates.auth)


@router.message(Text(text="Авторизоватся"))
async def authentication(message: Message, state: FSMContext):
    validated_data = await state.get_data()
    if await login(validated_data, message.from_user.id) is True:
        await message.answer(
            f'Авторизация прошла успешно\n'
            f'Добро пожаловать в Главное меню',
            reply_markup=management_keyboards.menu.as_markup(resize_keyboard=True)
        )
        await state.clear()
    else:
        await message.answer(
            f'Ошибка авторизации, попробуйте еще\n'
            f'Не забудьте убедится в правильности введенных данных',
            reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True)
        )


















