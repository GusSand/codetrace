from logging import getLogger
from typing import Iterable

import jsonpatch

logger = getLogger(__name__)


def patch(base: <FILL>, __tmp0):
    return jsonpatch.JsonPatch(__tmp0).apply(base)
