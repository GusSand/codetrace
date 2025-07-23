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

    def __tmp4(__tmp0, __tmp8: Dict[str, Any]) :
        __tmp0.select_keys = __tmp8.get("select_keys", None)
        __tmp0.ignore_case = __tmp8.get("ignore_case", False)

        # NOTE: Also checks that the regex isn't an empty string (which would erroneously match everything)
        regex_str = __tmp8.get("regex", None)
        __tmp0.regex = (
            re.compile(
                regex_str, (re.IGNORECASE if __tmp0.ignore_case else 0) | re.UNICODE
            )
            if regex_str
            else None
        )

    def match(__tmp0, e: <FILL>) :
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
    events: List[Event], __tmp6: List[Tuple[__typ2, __typ0]]
) :
    return [_categorize_one(e, __tmp6) for e in events]


def _categorize_one(e: Event, __tmp6) -> Event:
    e.data["$category"] = _pick_category(
        [_cls for _cls, rule in __tmp6 if rule.match(e)]
    )
    return e


def __tmp2(events, __tmp6: List[Tuple[Tag, __typ0]]) -> List[Event]:
    return [__tmp7(e, __tmp6) for e in events]


def __tmp7(e, __tmp6) -> Event:
    e.data["$tags"] = [_cls for _cls, rule in __tmp6 if rule.match(e)]
    return e


def _pick_category(__tmp3) :
    return reduce(__tmp1, __tmp3, ["Uncategorized"])


def __tmp1(__tmp5, t2: __typ2) -> __typ2:
    # t1 will be the accumulator when used in reduce
    # Always bias against t1, since it could be "Uncategorized"
    return t2 if len(t2) >= len(__tmp5) else __tmp5
