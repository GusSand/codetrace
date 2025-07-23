from typing import TypeAlias
__typ0 : TypeAlias = "State"
"""Location helpers for Home Assistant."""

from typing import Sequence

from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import State
from homeassistant.util import location as loc_util


def __tmp4(__tmp0) -> bool:
    """Test if state contains a valid location.

    Async friendly.
    """
    return (isinstance(__tmp0, __typ0) and
            isinstance(__tmp0.attributes.get(ATTR_LATITUDE), float) and
            isinstance(__tmp0.attributes.get(ATTR_LONGITUDE), float))


def __tmp3(__tmp2: <FILL>, longitude: float,
            __tmp1: Sequence[__typ0]) -> __typ0:
    """Return closest state to point.

    Async friendly.
    """
    with_location = [__tmp0 for __tmp0 in __tmp1 if __tmp4(__tmp0)]

    if not with_location:
        return None

    return min(
        with_location,
        key=lambda __tmp0: loc_util.distance(
            __tmp2, longitude, __tmp0.attributes.get(ATTR_LATITUDE),
            __tmp0.attributes.get(ATTR_LONGITUDE))
    )
