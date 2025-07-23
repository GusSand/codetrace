import re
from typing import List

from ajapaik.ajapaik.models import Dating


def __tmp1(date_accuracy_in: <FILL>):
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


def transform_fotis_persons_response(__tmp0: str) -> List[str]:
    __tmp0 = __tmp0.strip().strip(";")

    if ";" in __tmp0:
        persons = __tmp0.strip().split(";")
    else:
        persons = [__tmp0]

    result = []
    for person in persons:
        person = person.strip()
        match = re.match(r'\b(\w+(?:\s*\w*))\s+\1\b', person)
        if match:
            result.append(match.groups()[0])
        elif person:
            result.append(person)

    return list(set(result))
