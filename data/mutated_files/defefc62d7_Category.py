from typing import TypeAlias
__typ0 : TypeAlias = "Event"
__typ1 : TypeAlias = "bool"
from typing import Pattern, List, Iterable, Tuple, Dict, Optional, Any
from functools import reduce
import re

from aw_core import Event


Tag = str
Category = List[str]


class Rule:
    regex: Optional[Pattern]
    select_keys: Optional[List[str]]
    ignore_case: __typ1

    def __init__(__tmp0, __tmp2: Dict[str, Any]) -> None:
        __tmp0.select_keys = __tmp2.get("select_keys", None)
        __tmp0.ignore_case = __tmp2.get("ignore_case", False)

        # NOTE: Also checks that the regex isn't an empty string (which would erroneously match everything)
        regex_str = __tmp2.get("regex", None)
        __tmp0.regex = (
            re.compile(
                regex_str, (re.IGNORECASE if __tmp0.ignore_case else 0) | re.UNICODE
            )
            if regex_str
            else None
        )

    def match(__tmp0, e: __typ0) -> __typ1:
        if __tmp0.select_keys:
            values = [e.data.get(key, None) for key in __tmp0.select_keys]
        else:
            values = list(e.data.values())
        if __tmp0.regex:
            for val in values:
                if isinstance(val, str) and __tmp0.regex.search(val):
                    return True
        return False


def __tmp7(
    __tmp11: List[__typ0], __tmp10: List[Tuple[Category, Rule]]
) -> List[__typ0]:
    return [__tmp3(e, __tmp10) for e in __tmp11]


def __tmp3(e: __typ0, __tmp10: List[Tuple[Category, Rule]]) -> __typ0:
    e.data["$category"] = __tmp8(
        [_cls for _cls, rule in __tmp10 if rule.match(e)]
    )
    return e


def __tmp4(__tmp11: List[__typ0], __tmp10: List[Tuple[Tag, Rule]]) -> List[__typ0]:
    return [__tmp12(e, __tmp10) for e in __tmp11]


def __tmp12(e, __tmp10: List[Tuple[Tag, Rule]]) -> __typ0:
    e.data["$tags"] = [_cls for _cls, rule in __tmp10 if rule.match(e)]
    return e


def __tmp8(__tmp5: Iterable[Category]) -> Category:
    return reduce(__tmp1, __tmp5, ["Uncategorized"])


def __tmp1(__tmp9: <FILL>, __tmp6: Category) -> Category:
    # t1 will be the accumulator when used in reduce
    # Always bias against t1, since it could be "Uncategorized"
    return __tmp6 if len(__tmp6) >= len(__tmp9) else __tmp9
