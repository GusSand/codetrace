from typing import Dict, NamedTuple, Tuple, Union, overload


class __typ0(NamedTuple):
    latitude: float
    longitude: float


@overload
def __tmp1(__tmp0: <FILL>) :
    ...


@overload
def __tmp1(__tmp0: Union[Dict[str, float], Tuple[float, float]]) :
    ...


def __tmp1(__tmp0):
    if isinstance(__tmp0, dict):
        return __typ0(**__tmp0)
    elif isinstance(__tmp0, tuple):
        return __typ0(*__tmp0)
    else:
        return None
