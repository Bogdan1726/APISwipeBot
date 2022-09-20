from aiogram import types, Router
from aiogram.filters import Command, Text
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from settings.config import redis
from database.requests import is_authenticated, logout
from keyboards import base_keyboard
from aiogram.utils.i18n import gettext as _

router = Router()


async def set_language(language, user):
    if language not in ['Украинский', 'Русский']:
        return False
    else:
        if language == 'Украинский':
            await redis.set(f'user-{user}', 'uk')
        if language == 'Русский':
            await redis.set(f'user-{user}', 'ru')
        value = await redis.get(f'user-{user}')
        print(f'set-{value}')
        return value.decode()


class BaseStates(StatesGroup):
    start = State()
    language = State()


@router.message(Command(commands=["start"]))
@router.message(Text(text="К выбору языка"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        f'Здравствуйте {message.from_user.first_name} пожалуйста выберите язык чтобы продолжить',
        reply_markup=base_keyboard.language)
    await state.set_state(BaseStates.language)


@router.message(BaseStates.language)
async def command_start(message: Message, state: FSMContext):
    if await set_language(message.text, message.from_user.id):
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True))
    else:
        await message.answer(
            _('Нет такой команды')
        )
        await state.set_state(BaseStates.start)


@router.message(Text(text="Выход"))
async def command_start(message: Message, state: FSMContext):
    if is_authenticated(message.from_user.id):
        logout(message.from_user.id)
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True))
        await state.set_state(BaseStates.start)


@router.message(Text(text="Отмена"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить.'),
        reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True))
    await state.set_state(BaseStates.start)
