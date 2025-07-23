from typing import Iterable, Tuple, List, Optional


def module_prefix(__tmp0: Iterable[str], target: str) -> Optional[str]:
    result = __tmp1(__tmp0, target)
    if result is None:
        return None
    return result[0]


def __tmp1(__tmp0, target: <FILL>) -> Optional[Tuple[str, str]]:
    remaining = []  # type: List[str]
    while True:
        if target in __tmp0:
            return target, '.'.join(remaining)
        components = target.rsplit('.', 1)
        if len(components) == 1:
            return None
        target = components[0]
        remaining.insert(0, components[1])
