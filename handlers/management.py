from aiogram import types, Router
from aiogram.client.session import aiohttp
from aiogram.filters import Command, Text
from aiogram.types import Message
from api_requests.user import UserApiClient
from database.requests import is_authenticated, get_token
from keyboards import base_keyboard, authentication_keyboard, management_keyboards
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hide_link
from aiogram.utils.i18n import gettext as _
from aiogram import html
from aiogram.utils.i18n import lazy_gettext as __

from settings.config import HOST

router = Router()


# region profile

@router.message(Text(text="Профиль"))
async def user_profile(message: Message, state: FSMContext):
    user = message.from_user.id
    user_client = UserApiClient(user)
    if is_authenticated(user):
        data = await user_client.profile()
        await message.answer(
            _('Avatar: {logo}\n'
              'Имя: {first_name}\n'
              'Фамилия: {last_name}\n'
              'Телефон: {phone}\n'
              'E-mail: {email}').format(
                first_name=html.quote(data.get('first_name')),
                last_name=html.quote(data.get('last_name')),
                phone=html.quote(data.get('phone')) if data.get('phone') else "Нет даных",
                email=html.quote(data.get('email')),
                logo=hide_link(str('http://137.184.201.122' + data.get('profile_image'))),
            ), parse_mode="HTML",
            reply_markup=management_keyboards.get_profile_keyboard()
        )
    else:
        await message.answer(
            'Пожалуйста войдите или зарегистрируйтесь чтобы продолжить',
            reply_markup=base_keyboard.get_base_keyboard()
        )

# endregion profile
