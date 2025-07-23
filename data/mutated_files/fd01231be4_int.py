from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "bool"
def __tmp0(__tmp2) :
    return __typ0 == type(__tmp2) and not __tmp2.startswith('_')


def get_day_count(__tmp1: <FILL>, __tmp3: int) :
    return {
        1: 31,
        2: 29 if __tmp1 % 4 == 0 and __tmp1 % 400 != 0 else 28,
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
