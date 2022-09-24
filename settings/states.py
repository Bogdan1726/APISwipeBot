from aiogram.fsm.state import StatesGroup, State


class BaseStates(StatesGroup):
    start = State()
    language = State()


class ProfileStates(StatesGroup):
    profile = State()
    edit_profile = State()
    ads = State()
    edit_fields = State()
    email = State()
    phone = State()
    first_name = State()
    last_name = State()

