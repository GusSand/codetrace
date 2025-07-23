import logging
from typing import List
import re

from aw_core.models import Event

logger = logging.getLogger(__name__)


def __tmp0(
    __tmp4, key: str, vals, exclude=False
) :
    def __tmp2(__tmp1):
        return key in __tmp1.data and __tmp1.data[key] in vals

    if exclude:
        return [e for e in __tmp4 if not __tmp2(e)]
    else:
        return [e for e in __tmp4 if __tmp2(e)]


def filter_keyvals_regex(__tmp4, key, __tmp3: <FILL>) -> List[Event]:
    r = re.compile(__tmp3)

    def __tmp2(__tmp1):
        return key in __tmp1.data and bool(r.findall(__tmp1.data[key]))

    return [e for e in __tmp4 if __tmp2(e)]
