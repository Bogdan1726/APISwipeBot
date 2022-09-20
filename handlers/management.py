from aiogram import types, Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command, Text
from aiogram.types import Message
from api_requests.user import login, profile
from database.requests import is_authenticated, get_token
from keyboards import base_keyboard, authentication_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hide_link

router = Router()


# class AuthenticationStates(StatesGroup):
#     write_mail = State()
#     write_password = State()
#     auth = State()

# region profile
@router.message(Text(text="Профиль"))
async def user_profile(message: Message, state: FSMContext):
    user = message.from_user.id
    if is_authenticated(user):
        if await profile(user):
            data = await profile(user)
            await message.answer(
                f'Имя: {data.get("first_name")}\n'
                f'Фамилия: {data.get("last_name")}\n'
                f'Телефон: {data.get("phone") if data.get("phone") else "Нет даных"}\n'
                f'E-mail: {data.get("email")}',
                reply_markup=management_keyboards.profile
            )
        else:
            await message.answer(
                'Пожалуйста войдите или зарегистрируйтесь чтобы продолжить',
                reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True)
            )

            # endregion profile
