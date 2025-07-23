from typing import TypeAlias
__typ1 : TypeAlias = "bool"
from typing import Pattern, List, Iterable, Tuple, Dict, Optional, Any
from functools import reduce
import re

from aw_core import Event


Tag = str
__typ2 = List[str]


class __typ0:
    regex: Optional[Pattern]
    select_keys: Optional[List[str]]
    ignore_case: __typ1

    def __init__(__tmp0, __tmp1: Dict[str, Any]) -> None:
        __tmp0.select_keys = __tmp1.get("select_keys", None)
        __tmp0.ignore_case = __tmp1.get("ignore_case", False)

        # NOTE: Also checks that the regex isn't an empty string (which would erroneously match everything)
        regex_str = __tmp1.get("regex", None)
        __tmp0.regex = (
            re.compile(
                regex_str, (re.IGNORECASE if __tmp0.ignore_case else 0) | re.UNICODE
            )
            if regex_str
            else None
        )

    def match(__tmp0, e: Event) -> __typ1:
        if __tmp0.select_keys:
            values = [e.data.get(key, None) for key in __tmp0.select_keys]
        else:
            values = list(e.data.values())
        if __tmp0.regex:
            for val in values:
                if isinstance(val, str) and __tmp0.regex.search(val):
                    return True
        return False


def categorize(
    __tmp9: List[Event], __tmp8
) -> List[Event]:
    return [__tmp3(e, __tmp8) for e in __tmp9]


def __tmp3(e, __tmp8: List[Tuple[__typ2, __typ0]]) -> Event:
    e.data["$category"] = __tmp6(
        [_cls for _cls, rule in __tmp8 if rule.match(e)]
    )
    return e


def tag(__tmp9, __tmp8: List[Tuple[Tag, __typ0]]) -> List[Event]:
    return [__tmp10(e, __tmp8) for e in __tmp9]


def __tmp10(e: <FILL>, __tmp8: List[Tuple[Tag, __typ0]]) -> Event:
    e.data["$tags"] = [_cls for _cls, rule in __tmp8 if rule.match(e)]
    return e


def __tmp6(__tmp5) -> __typ2:
    return reduce(__tmp2, __tmp5, ["Uncategorized"])


def __tmp2(__tmp7: __typ2, __tmp4: __typ2) -> __typ2:
    # t1 will be the accumulator when used in reduce
    # Always bias against t1, since it could be "Uncategorized"
    return __tmp4 if len(__tmp4) >= len(__tmp7) else __tmp7
