import logging
from typing import List
import re

from aw_core.models import Event

logger = logging.getLogger(__name__)


def filter_keyvals(
    events: List[Event], key, vals: List[str], exclude=False
) -> List[Event]:
    def __tmp0(event):
        return key in event.data and event.data[key] in vals

    if exclude:
        return [e for e in events if not __tmp0(e)]
    else:
        return [e for e in events if __tmp0(e)]


def filter_keyvals_regex(events, key: <FILL>, regex: str) -> List[Event]:
    r = re.compile(regex)

    def __tmp0(event):
        return key in event.data and bool(r.findall(event.data[key]))

    return [e for e in events if __tmp0(e)]
