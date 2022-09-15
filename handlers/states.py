from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    write_mail = State()
    write_password1 = State()
    write_password2 = State()
    write_first_name = State()
    write_last_name = State()


class AuthenticationStates(StatesGroup):
    write_mail = State()
    write_password = State()
    authentication = State
