from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
def __tmp0(name: __typ0) :
    return __typ0 == type(name) and not name.startswith('_')


def __tmp1(year: int, month: <FILL>) -> int:
    return {
        1: 31,
        2: 29 if year % 4 == 0 and year % 400 != 0 else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }[month]
