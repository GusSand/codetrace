from typing import TypeAlias
__typ0 : TypeAlias = "State"
__typ1 : TypeAlias = "bool"
"""Location helpers for Home Assistant."""

from typing import Optional, Sequence

from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import State
from homeassistant.util import location as loc_util


def has_location(__tmp1: __typ0) -> __typ1:
    """Test if state contains a valid location.

    Async friendly.
    """
    return (isinstance(__tmp1, __typ0) and
            isinstance(__tmp1.attributes.get(ATTR_LATITUDE), float) and
            isinstance(__tmp1.attributes.get(ATTR_LONGITUDE), float))


def __tmp4(__tmp3: <FILL>, __tmp0: float,
            __tmp2) -> Optional[__typ0]:
    """Return closest state to point.

    Async friendly.
    """
    with_location = [__tmp1 for __tmp1 in __tmp2 if has_location(__tmp1)]

    if not with_location:
        return None

    return min(
        with_location,
        key=lambda __tmp1: loc_util.distance(
            __tmp1.attributes.get(ATTR_LATITUDE),
            __tmp1.attributes.get(ATTR_LONGITUDE),
            __tmp3, __tmp0)
    )
