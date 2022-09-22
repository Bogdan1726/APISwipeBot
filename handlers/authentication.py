from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from api_requests.user import UserApiClient
from keyboards import management_keyboards, authentication_keyboard, base_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class AuthenticationStates(StatesGroup):
    login = State()
    email = State()
    password = State()
    auth = State()


@router.message(Text(text="Вход"))
@router.message(AuthenticationStates.login)
async def login_email(message: Message, state: FSMContext) -> None:
    await state.set_state(AuthenticationStates.email)
    await message.answer(
        "Введите e-mail:",
        reply_markup=authentication_keyboard.cancel
    )


@router.message(AuthenticationStates.email)
async def login_password(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text.lower())
    await state.set_state(AuthenticationStates.password)
    await message.answer(
        "Введите пароль:",
        reply_markup=authentication_keyboard.cancel
    )

@router.message(AuthenticationStates.password)
async def authentication(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await state.set_state(AuthenticationStates.auth)
    data = await state.get_data()
    await message.answer(
        f'Ваши данные для входа \n'
        f'E-mail: {data.get("email")}\n'
        f'Пароль: {data.get("password")}\n'
        f'Если все верно нажмите кнопку «Авторизоватся»\n'
        f'В противном случае нажмите «Отмена» и повторите попытку',
        reply_markup=authentication_keyboard.auth
    )


@router.message(Text(text="Авторизоватся"))
async def authentication(message: Message, state: FSMContext) -> None:
    validated_data = await state.get_data()
    user_client = UserApiClient(message.from_user.id)
    response = await user_client.login(validated_data)
    print(response)
    if response:
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
