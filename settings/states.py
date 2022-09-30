from aiogram.fsm.state import StatesGroup, State


class BaseStates(StatesGroup):
    start = State()
    language = State()


class ProfileStates(StatesGroup):
    profile = State()
    edit_profile = State()
    edit_fields = State()
    email = State()
    phone = State()
    first_name = State()
    last_name = State()
    photo = State()
    ads = State()
    edit_ads = State()
    add_ads = State()
    add_ads_purpose = State()
    add_ads_address = State()
    add_ads_house = State()
    add_ads_area = State()
    add_ads_area_kitchen = State()
    add_ads_room = State()
    add_ads_condition = State()
    add_ads_description = State()
    add_ads_price = State()
    test = State()


class RegistrationStates(StatesGroup):
    start_registration = State()
    write_mail = State()
    write_password1 = State()
    write_password2 = State()
    write_first_name = State()
    write_last_name = State()
    register = State()
    register_edit_data = State()
    edit_email = State()
    edit_password = State()
    edit_first_name = State()
    edit_last_name = State()


class AuthenticationStates(StatesGroup):
    login = State()
    email = State()
    password = State()
    auth = State()
