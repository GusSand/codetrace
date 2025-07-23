from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""This module contains mathematical functions needed to generate
data."""

__author__ = "Miroslav Nikolic and Novak Boskov"
__copyright__ = "Typhoon HIL Inc."
__license__ = "MIT"

import json
from math import pi, cos
from functools import partial
from typing import Optional, Tuple, List, Dict, Union


def __tmp7(t: __typ0) -> Optional[__typ0]:
    if t < 7 or 23 <= t <= 24:
        return 3
    elif 7 <= t < 23:
        return 8
    else:
        raise Exception('Time should be between 0 and 24')


def __tmp2(t) -> Optional[__typ0]:
    if 0 <= t < 11 or 17 <= t <= 24:
        return 3
    elif 11 <= t < 17:
        return 0
    else:
        raise Exception('Time should be between 0 and 24')


def __tmp3(t, load_scaling=1.0, load_scaling_prev=1.0) -> __typ0:
    if 3 <= t < 13:
        return (load_scaling * 1.5) * (cos(1/5 * pi * (t - 8)) + 1) + 2
    elif 13 <= t <= 24:
        return (load_scaling * 3) * (cos(1/7 * pi * (t - 20)) + 1) + 2
    elif 0 <= t < 3:
        return (load_scaling_prev * 3) * (cos(1/7 * pi * (t + 4)) + 1) + 2
    else:
        raise Exception('Time should be between 0 and 24')


def __tmp0(t: __typ0, solar_scaling=1.0) :
    if 7 <= t < 19:
        return (solar_scaling * 2) * (cos(1/6 * pi * (t - 13)) + 1)
    elif 0 <= t < 7 or 19 <= t <= 24:
        return 0
    else:
        raise Exception('Time should be between 0 and 24')


def __tmp5(__tmp1: int, __tmp4: <FILL>) -> __typ0:
    """Converts sample number to day time."""
    return __tmp4 / __tmp1


def __tmp6(__tmp1, load_scaling=1.0,
                load_scaling_prev=1.0, solar_scaling=1.0, blackouts=[]) \
    -> Tuple[str, List[Dict[str, Union[__typ0, bool]]]]:
    """Generates ideal profile."""
    to_time = partial(__tmp5, __tmp1)
    data = []

    for s in range(__tmp1*24):
        t = to_time(s)
        gs = 1
        if blackouts:
            for blackout in blackouts:
                if blackout[0] <= t < blackout[1]:
                    gs = 0
        data.append({'gridStatus': gs,
                     'buyingPrice': __tmp7(t),
                     'sellingPrice': __tmp2(t),
                     'currentLoad': __tmp3(t,
                                                 load_scaling,
                                                 load_scaling_prev),
                     'solarProduction': __tmp0(t, solar_scaling)})

    return json.dumps(data), data
