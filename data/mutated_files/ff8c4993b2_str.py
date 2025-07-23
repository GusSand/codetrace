import re
from typing import List

from ajapaik.ajapaik.models import Dating


def __tmp0(date_accuracy_in):
    if date_accuracy_in == 'Sajand':
        date_accuracy = Dating.CENTURY
        date_format = '%Y'
    elif date_accuracy_in == 'Kümnend':
        date_accuracy = Dating.DECADE
        date_format = '%Y'
    elif date_accuracy_in == 'Aasta':
        date_accuracy = Dating.YEAR
        date_format = '%Y'
    elif date_accuracy_in == 'Kuu':
        date_accuracy = Dating.MONTH
        date_format = '%Y.%m'
    elif date_accuracy_in == 'Kuupäev':
        date_accuracy = Dating.DAY
        date_format = '%Y.%m.%d'
    else:
        date_accuracy = None
        date_format = '%Y.%m.%d'

    return date_accuracy, date_format


def transform_fotis_persons_response(persons_str: <FILL>) -> List[str]:
    persons_str = persons_str.strip().strip(";")

    if ";" in persons_str:
        persons = persons_str.strip().split(";")
    else:
        persons = [persons_str]

    result = []
    for person in persons:
        person = person.strip()
        match = re.match(r'\b(\w+(?:\s*\w*))\s+\1\b', person)
        if match:
            result.append(match.groups()[0])
        elif person:
            result.append(person)

    return list(set(result))
