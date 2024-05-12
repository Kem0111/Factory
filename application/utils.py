import re

import requests
from bitrix24 import Bitrix24
from django.core.exceptions import ValidationError


def validate_phone(value):
    rule = re.compile('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
    if not rule.match(value):
        raise ValidationError(f'Некорректный номер телефона: {value}')


def check_deals_address(city, street):
    bx24 = Bitrix24('https://brickus62.bitrix24.ru/rest/6139/amz8rvj6qtmxf2es')
    result = bx24.callMethod('crm.deal.list')
    for i in result:
        if i['COMMENTS'] is None:
            continue
        if city.lower() in i['COMMENTS'].lower() and street.lower() in i['COMMENTS'].lower():
            return True
    return False


def create_deals(city, street, house, email):
    bx24 = Bitrix24('https://brickus62.bitrix24.ru/rest/6139/amz8rvj6qtmxf2es')
    result = bx24.callMethod('crm.lead.add', fields={
        'COMMENTS': f'Адрес объекта: \n\n{city}, {street}, {house}\n\nНаименование\n\nEmail: {email}',
        'CATEGORY_ID': '9',
    })
    return result
