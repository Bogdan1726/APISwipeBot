import re
from aiogram.utils.i18n import gettext as _


def validate_email(email: str) -> bool:
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(pattern, email) is None:
        return False
    else:
        return True


def validate_password(password: str) -> bool:
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    if pattern_password.match(password):
        return True
    else:
        return False


def validate_name(value: str) -> bool:
    if value.isalpha() and value.istitle() and 2 <= len(value) <= 24:
        return True
    return False


def validate_phone(value: str) -> bool:
    pattern = r'^(?:\+38)?(0\d{9})$'
    if re.match(pattern, value) is None:
        return False
    return True


def validate_image(value) -> bool:
    if value.height > 300 or value.width > 300 or value.file_size > 19900000:
        return False
    return True


def validate_image_ads(value) -> bool:
    if value.height > 800 or value.width > 800 or value.file_size > 19900000:
        return False
    return True


def validate_purpose(purpose: str) -> bool:
    if purpose in [_('Дом'), _('Квартира'), _('Коммерческие помещения'), _('Офисное помещение')]:
        return True
    else:
        return False


def validate_address(address: str) -> bool:
    if len(address) > 10 and address.isspace() is False:
        return bool(re.search('[а-яА-Я0-9]', address))
    else:
        return False


def validate_house(house: str) -> bool:
    if house in ['ЖК 1', 'ЖК 2', 'ЖК 3', 'ЖК 4', 'ЖК 5']:
        return True
    else:
        return False


def validate_area(area: str) -> bool:
    try:
        if 0 < float(area) < 1000:
            return True
        return False
    except ValueError:
        return False


def validate_area_edit_ads(area: str, area_kitchen: str) -> bool:
    try:
        if 0 < float(area) < 1000 and 0 < float(area_kitchen) < 1000 and float(area) > float(area_kitchen):
            return True
        return False
    except ValueError:
        return False


def validate_room(room: str) -> bool:
    if room.isdigit():
        if int(room) <= 10:
            return True
        else:
            return False
    else:
        return False


def validate_condition(condition: str) -> bool:
    if condition in [_("Черновая"), _("Ремонт от застройщика"), _("В жилом состоянии")]:
        return True
    else:
        return False


def validate_layout(layout: str) -> bool:
    if layout in [_("Студия, санузел"), _("Классическая"), _("Европланировка"), _("Свободная")]:
        return True
    else:
        return False


def validate_founding_document(founding_document: str) -> bool:
    if founding_document in [_("Собственность"), _("Свидетельство о праве на наследство")]:
        return True
    else:
        return False


def validate_description(description: str) -> bool:
    if len(description) >= 20 and description.isspace() is False:
        return bool(re.search('[а-яА-Я]', description))
    else:
        return False


def validate_price(price: str) -> bool:
    price = price.replace(' ', '')
    if price.isdigit():
        if 100000000 > int(price) >= 0:
            return True
        else:
            return False
    else:
        return False


def parse_ads_data(data: dict) -> dict:
    founding_document_dic = {
        "Власність": "Собственность",
        "Свідоцтво про право на спадщину": "Свидетельство о праве на наследство"
    }
    layout_dic = {
        "Студія, санвузол": "Студия, санузел",
        "Класична": "Классическая",
        "Європланування": "Европланировка",
        'Вільна': "Свободная"
    }
    purpose_dic = {
        "Будинок": "Дом",
        "Квартира": "Квартира",
        "У житловому стані": "Коммерческие помещения",
        'Офісне приміщення': "Коммерческие помещения"
    }
    condition_dic = {
        "Чорнова": "Черновая",
        "Ремонт від забудовника": "Ремонт от застройщика",
        "У житловому стані": "В жилом состоянии"
    }
    residential_complex_dic = {
        "ЖК 1": 1,
        "ЖК 2": 2,
        "ЖК 3": 3,
        "ЖК 4": 4,
        "ЖК 5": 5,
    }

    condition = data.get('condition')
    purpose = data.get('purpose')
    residential_complex = data.get('house')
    layout = data.get('layout')
    founding_document = data.get('founding_document')

    if condition_dic.get(condition):
        _condition = condition_dic.get(condition)
        data['condition'] = _condition
    if purpose_dic.get(purpose):
        _purpose = purpose_dic.get(purpose)
        data['purpose'] = _purpose
    if residential_complex_dic.get(residential_complex):
        _residential_complex = residential_complex_dic.get(residential_complex)
        data['house'] = _residential_complex
    if layout_dic.get(layout):
        _layout = layout_dic.get(layout)
        data['layout'] = _layout
    if founding_document_dic.get(founding_document):
        _founding_document = founding_document_dic.get(founding_document)
        data['founding_document'] = _founding_document
    return data
