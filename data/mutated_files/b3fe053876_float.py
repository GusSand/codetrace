from typing import TypeAlias
__typ0 : TypeAlias = "State"
__typ1 : TypeAlias = "bool"
"""Location helpers for Home Assistant."""

from typing import Sequence

from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.core import State
from homeassistant.util import location as loc_util


def __tmp1(state) :
    """Test if state contains a valid location.

    Async friendly.
    """
    return (isinstance(state, __typ0) and
            isinstance(state.attributes.get(ATTR_LATITUDE), float) and
            isinstance(state.attributes.get(ATTR_LONGITUDE), float))


def __tmp2(latitude: float, longitude: <FILL>,
            __tmp0: Sequence[__typ0]) -> __typ0:
    """Return closest state to point.

    Async friendly.
    """
    with_location = [state for state in __tmp0 if __tmp1(state)]

    if not with_location:
        return None

    return min(
        with_location,
        key=lambda state: loc_util.distance(
            latitude, longitude, state.attributes.get(ATTR_LATITUDE),
            state.attributes.get(ATTR_LONGITUDE))
    )
