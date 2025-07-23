import logging
from typing import List
import re

from aw_core.models import Event

logger = logging.getLogger(__name__)


def __tmp0(
    events, key: <FILL>, vals, exclude=False
) :
    def predicate(event):
        return key in event.data and event.data[key] in vals

    if exclude:
        return [e for e in events if not predicate(e)]
    else:
        return [e for e in events if predicate(e)]


def filter_keyvals_regex(events, key, regex: str) :
    r = re.compile(regex)

    def predicate(event):
        return key in event.data and bool(r.findall(event.data[key]))

    return [e for e in events if predicate(e)]
