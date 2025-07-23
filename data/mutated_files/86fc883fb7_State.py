from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""Location helpers for Home Assistant."""

from typing import Sequence

from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import State
from homeassistant.util import location as loc_util


def __tmp5(__tmp1: <FILL>) -> __typ0:
    """Test if state contains a valid location.

    Async friendly.
    """
    return (isinstance(__tmp1, State) and
            isinstance(__tmp1.attributes.get(ATTR_LATITUDE), float) and
            isinstance(__tmp1.attributes.get(ATTR_LONGITUDE), float))


def __tmp3(__tmp4: float, __tmp0,
            __tmp2: Sequence[State]) -> State:
    """Return closest state to point.

    Async friendly.
    """
    with_location = [__tmp1 for __tmp1 in __tmp2 if __tmp5(__tmp1)]

    if not with_location:
        return None

    return min(
        with_location,
        key=lambda __tmp1: loc_util.distance(
            __tmp4, __tmp0, __tmp1.attributes.get(ATTR_LATITUDE),
            __tmp1.attributes.get(ATTR_LONGITUDE))
    )
