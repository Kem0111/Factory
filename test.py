from bitrix24 import *

bx24 = Bitrix24('https://brickus62.bitrix24.ru/rest/6139/amz8rvj6qtmxf2es')

result = bx24.callMethod('crm.deal.list')
for i in result:
    if i['COMMENTS'] is None:
        continue
    if 'тест' in i['COMMENTS'] and 'тест' in i['COMMENTS']:
        print(i)
print(result)