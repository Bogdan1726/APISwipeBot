from aiogram import types, Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards import base_keyboard

router = Router()


@router.message(Command(commands=["start"]))
async def command_start(message: Message) -> None:
    await message.answer(
        'Пожалуйста войдите или зарегистрируйтесь чтобы продолжить.',
        reply_markup=base_keyboard.keyboard)


@router.message(Text(text="Отмена"))
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        'Пожалуйста войдите или зарегистрируйтесь чтобы продолжить.',
        reply_markup=base_keyboard.keyboard)
