"""Location helpers for Home Assistant."""

from typing import Optional, Sequence

from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import State
from homeassistant.util import location as loc_util


def __tmp0(__tmp2: <FILL>) -> bool:
    """Test if state contains a valid location.

    Async friendly.
    """
    return (isinstance(__tmp2, State) and
            isinstance(__tmp2.attributes.get(ATTR_LATITUDE), float) and
            isinstance(__tmp2.attributes.get(ATTR_LONGITUDE), float))


def closest(__tmp1: float, longitude: float,
            states: Sequence[State]) :
    """Return closest state to point.

    Async friendly.
    """
    with_location = [__tmp2 for __tmp2 in states if __tmp0(__tmp2)]

    if not with_location:
        return None

    return min(
        with_location,
        key=lambda __tmp2: loc_util.distance(
            __tmp2.attributes.get(ATTR_LATITUDE),
            __tmp2.attributes.get(ATTR_LONGITUDE),
            __tmp1, longitude)
    )
