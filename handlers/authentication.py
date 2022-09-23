from aiogram import Router, F
from aiogram.types import Message
from api_requests.user import UserApiClient
from keyboards import management_keyboards, authentication_keyboard, base_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.i18n import gettext as _
from aiogram import html
from aiogram.utils.i18n import lazy_gettext as __

router = Router()


class AuthenticationStates(StatesGroup):
    login = State()
    email = State()
    password = State()
    auth = State()


@router.message(F.text.lower() == __("вход"))
@router.message(AuthenticationStates.login)
async def login_email(message: Message, state: FSMContext) -> None:
    await state.set_state(AuthenticationStates.email)
    await message.answer(
        _("Введите e-mail:"),
        reply_markup=base_keyboard.get_cancel_keyboard()
    )


@router.message(AuthenticationStates.email)
async def login_password(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text.lower())
    await state.set_state(AuthenticationStates.password)
    await message.answer(
        _("Введите пароль:"),
        reply_markup=base_keyboard.get_cancel_keyboard()
    )


@router.message(AuthenticationStates.password)
async def authentication(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await state.set_state(AuthenticationStates.auth)
    data = await state.get_data()
    await message.answer(
        _('Ваши данные для входа \n'
          'E-mail: {email}\n'
          'Пароль: {password}\n'
          'Если все верно нажмите кнопку «Войти»\n'
          'В противном случае нажмите «Отмена» и повторите попытку').format(
            email=html.quote(data.get('email')),
            password=html.quote(data.get('password')),

        ),
        reply_markup=authentication_keyboard.get_auth_keyboard()
    )


@router.message(F.text.lower() == __("войти"))
async def authentication(message: Message, state: FSMContext) -> None:
    validated_data = await state.get_data()
    user_client = UserApiClient(message.from_user.id)
    response = await user_client.login(validated_data)
    if response:
        await message.answer(
            _('Авторизация прошла успешно\n'
              'Добро пожаловать в Главное меню'),
            reply_markup=management_keyboards.get_main_menu_keyboard()
        )
        await state.clear()
    else:
        await message.answer(
            _('Ошибка авторизации, попробуйте еще\n'
              'Не забудьте убедится в правильности введенных данных'),
            reply_markup=base_keyboard.get_base_keyboard()
        )
