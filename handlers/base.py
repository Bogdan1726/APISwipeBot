from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.requests import is_authenticated, logout
from keyboards import base_keyboard
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from settings.states import BaseStates

router = Router()


@router.message(Command(commands=["start"]))
@router.message(F.text.casefold() == __("к выбору языка"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        f'Здравствуйте {message.from_user.first_name} пожалуйста выберите язык чтобы продолжить',
        reply_markup=base_keyboard.get_language_keyboard())
    await state.set_state(BaseStates.language)


@router.message(F.text.casefold() == __("отмена"))
@router.message(BaseStates.language)
async def command_start(message: Message, state: FSMContext):
    await message.answer(
        _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
        reply_markup=base_keyboard.get_base_keyboard())
    await state.set_state(BaseStates.start)


@router.message(F.text.casefold() == __("выход"))
async def command_start(message: Message, state: FSMContext):
    if is_authenticated(message.from_user.id):
        logout(message.from_user.id)
        await message.answer(
            _('Пожалуйста войдите или зарегистрируйтесь чтобы продолжить'),
            reply_markup=base_keyboard.get_base_keyboard())
        await state.set_state(BaseStates.start)
