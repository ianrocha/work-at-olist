import re


def validate_phone_number(phone_number):
    if not re.match(r'^((10)|([1-9][1-9]))\d{8,9}$', phone_number):
        return False
    return True
