import re


def validate_email(email: str) -> bool:
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"
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
