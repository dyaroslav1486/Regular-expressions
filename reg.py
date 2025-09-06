from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

pattern = re.compile(
    r'(?:\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(?:\s*(?:доб\.?|\(доб\.)\s*\.?(\d+)\)?)?',
    re.IGNORECASE
)


def normalize(phone):
    m = pattern.search(phone)
    if not m:
        return None
    code, part1, part2, part3, ext = m.groups()
    result = f"+7({code}){part1}-{part2}-{part3}"
    if ext != None:
        result += f" доб.{ext}"
    return result

for data in contacts_list:
    abbreviation = (" ".join(data[:2])).split(" ")
    last_name = abbreviation[0]
    first_name = abbreviation[1]
    if len(abbreviation) >=3:
       surname = abbreviation [2]
    else: surname = ''
    organization = data[3]
    position = data[4]
    email = data[6]
    phone = normalize(data[5])
    

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)