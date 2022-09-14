from aiogram import types, Router
from aiogram.filters import Command, Text
from aiogram.types import Message


@router.message(Text(text="Вход"))
async def login(message: Message):
    await message.reply("Отличный выбор!", reply_markup=types.ReplyKeyboardRemove())
