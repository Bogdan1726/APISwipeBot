from aiogram import types, Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command, Text
from aiogram.types import Message
from keyboards import base_keyboard
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
        f'Ваши данные{data}',
        reply_markup=base_keyboard.auth
    )
    await state.set_state(AuthenticationStates.auth)


@router.message(Text(text="Авторизоватся"))
async def authentication(message: Message, state: FSMContext):
    validated_data = await state.get_data()
    data = {
        'email': validated_data.get('email'),
        'password': validated_data.get('password')
    }
    async with aiohttp.ClientSession() as session:
        response = await session.post(url='http://164.90.255.130/login/', data=data)
        if response.status == 200:
            body = await response.json()
            await message.answer(
                f'{body.get("access_token")}'
            )
        else:
            await message.answer(
                'Ошибка'
            )
        await state.clear()



