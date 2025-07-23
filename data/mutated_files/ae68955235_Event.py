from typing import Pattern, List, Iterable, Tuple, Dict, Optional, Any
from functools import reduce
import re

from aw_core import Event


Tag = str
__typ1 = List[str]


class __typ0:
    regex: Optional[Pattern]
    select_keys: Optional[List[str]]
    ignore_case: bool

    def __init__(__tmp0, rules: Dict[str, Any]) -> None:
        __tmp0.select_keys = rules.get("select_keys", None)
        __tmp0.ignore_case = rules.get("ignore_case", False)

        # NOTE: Also checks that the regex isn't an empty string (which would erroneously match everything)
        regex_str = rules.get("regex", None)
        __tmp0.regex = (
            re.compile(
                regex_str, (re.IGNORECASE if __tmp0.ignore_case else 0) | re.UNICODE
            )
            if regex_str
            else None
        )

    def match(__tmp0, e: Event) -> bool:
        if __tmp0.select_keys:
            values = [e.data.get(key, None) for key in __tmp0.select_keys]
        else:
            values = list(e.data.values())
        if __tmp0.regex:
            for val in values:
                if isinstance(val, str) and __tmp0.regex.search(val):
                    return True
        return False


def __tmp3(
    __tmp8: List[Event], __tmp7: List[Tuple[__typ1, __typ0]]
) -> List[Event]:
    return [__tmp2(e, __tmp7) for e in __tmp8]


def __tmp2(e: <FILL>, __tmp7: List[Tuple[__typ1, __typ0]]) -> Event:
    e.data["$category"] = _pick_category(
        [_cls for _cls, rule in __tmp7 if rule.match(e)]
    )
    return e


def tag(__tmp8: List[Event], __tmp7) -> List[Event]:
    return [__tmp9(e, __tmp7) for e in __tmp8]


def __tmp9(e, __tmp7) -> Event:
    e.data["$tags"] = [_cls for _cls, rule in __tmp7 if rule.match(e)]
    return e


def _pick_category(__tmp4) -> __typ1:
    return reduce(__tmp1, __tmp4, ["Uncategorized"])


def __tmp1(__tmp6: __typ1, __tmp5) -> __typ1:
    # t1 will be the accumulator when used in reduce
    # Always bias against t1, since it could be "Uncategorized"
    return __tmp5 if len(__tmp5) >= len(__tmp6) else __tmp6
