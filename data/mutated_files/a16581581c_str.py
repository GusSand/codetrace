from typing import TypeAlias
__typ0 : TypeAlias = "int"
def __tmp0(__tmp2: <FILL>) -> bool:
    return str == type(__tmp2) and not __tmp2.startswith('_')


def __tmp1(year: __typ0, __tmp3) -> __typ0:
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
    }[__tmp3]
