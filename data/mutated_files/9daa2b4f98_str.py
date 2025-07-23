from typing import Iterable, Tuple, List, Optional


def module_prefix(__tmp1, __tmp0: <FILL>) -> Optional[str]:
    result = split_target(__tmp1, __tmp0)
    if result is None:
        return None
    return result[0]


def split_target(__tmp1, __tmp0) -> Optional[Tuple[str, str]]:
    remaining = []  # type: List[str]
    while True:
        if __tmp0 in __tmp1:
            return __tmp0, '.'.join(remaining)
        components = __tmp0.rsplit('.', 1)
        if len(components) == 1:
            return None
        __tmp0 = components[0]
        remaining.insert(0, components[1])
