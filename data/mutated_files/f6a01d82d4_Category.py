from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "Event"
from typing import Pattern, List, Iterable, Tuple, Dict, Optional, Any
from functools import reduce
import re

from aw_core import Event


Tag = str
Category = List[str]


class __typ1:
    regex: Optional[Pattern]
    select_keys: Optional[List[str]]
    ignore_case: __typ2

    def __init__(__tmp0, __tmp1) :
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

    def match(__tmp0, e: __typ0) -> __typ2:
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
    __tmp6: List[__typ0], __tmp5: List[Tuple[Category, __typ1]]
) -> List[__typ0]:
    return [__tmp2(e, __tmp5) for e in __tmp6]


def __tmp2(e: __typ0, __tmp5: List[Tuple[Category, __typ1]]) -> __typ0:
    e.data["$category"] = _pick_category(
        [_cls for _cls, rule in __tmp5 if rule.match(e)]
    )
    return e


def tag(__tmp6: List[__typ0], __tmp5: List[Tuple[Tag, __typ1]]) -> List[__typ0]:
    return [__tmp7(e, __tmp5) for e in __tmp6]


def __tmp7(e, __tmp5: List[Tuple[Tag, __typ1]]) -> __typ0:
    e.data["$tags"] = [_cls for _cls, rule in __tmp5 if rule.match(e)]
    return e


def _pick_category(tags: Iterable[Category]) -> Category:
    return reduce(_pick_deepest_cat, tags, ["Uncategorized"])


def _pick_deepest_cat(__tmp4: Category, __tmp3: <FILL>) -> Category:
    # t1 will be the accumulator when used in reduce
    # Always bias against t1, since it could be "Uncategorized"
    return __tmp3 if len(__tmp3) >= len(__tmp4) else __tmp4
