from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


pattern = re.compile(
    r'(?:\+7|8)\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(?:\s*(?:доб\.?|\(доб\.)\s*\.?(\d+)\)?)?',
    re.IGNORECASE
)

def normalize(phone):
    if not phone or "нет номера" in phone.lower():
        return ""
    m = pattern.search(phone)
    if not m:
        return phone.strip()
    code, part1, part2, part3, ext = m.groups()
    result = f"+7({code}){part1}-{part2}-{part3}"
    if ext:
        result += f" доб.{ext}"
    return result


contacts_list_remake = []
for data in contacts_list:
    abbreviation = (" ".join(data[:3])).split()
    last_name = abbreviation[0] if len(abbreviation) > 0 else ""
    first_name = abbreviation[1] if len(abbreviation) > 1 else ""
    surname = abbreviation[2] if len(abbreviation) > 2 else ""
    phone = normalize(data[5])
    contacts = [last_name, first_name, surname, data[3], data[4], phone, data[6]]
    contacts_list_remake.append(contacts)


merged = {}

for row in contacts_list_remake:
    key = (row[0], row[1], row[2])  # (lastname, firstname, surname)
    if key not in merged:
        merged[key] = row
    else:
        existing = merged[key]
        for i in range(len(row)):
            if not existing[i] and row[i]:
                existing[i] = row[i]


contacts_list_final = list(merged.values())

with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_final)

print(f"Готово! Было {len(contacts_list)} строк, стало {len(contacts_list_final)}.")
