from aiogram import types, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards import base_keyboard
from aioredis import Redis

router = Router()
redis = Redis()


class BaseStates(StatesGroup):
    language = State()
    start = State()


@router.message(Command(commands=["start"]))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        f'Здравствуйте {message.from_user.first_name} пожалуйста выберите язык чтобы продолжить',
        reply_markup=base_keyboard.language)
    await state.set_state(BaseStates.language)


@router.message(BaseStates.language)
async def command_start(message: Message, state: FSMContext):
    language = message.text
    await message.answer(
        f'Пожалуйста войдите или зарегистрируйтесь чтобы продолжить',
        reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True))
    await state.set_state(BaseStates.start)


@router.message(Text(text="Отмена"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        'Пожалуйста войдите или зарегистрируйтесь чтобы продолжить.',
        reply_markup=base_keyboard.keyboard.as_markup(resize_keyboard=True))
    await state.set_state(BaseStates.start)


@router.message(Text(text="К выбору языка"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        'Пожалуйста выберите язык чтобы продолжить.',
        reply_markup=base_keyboard.language)
    await state.set_state(BaseStates.language)
