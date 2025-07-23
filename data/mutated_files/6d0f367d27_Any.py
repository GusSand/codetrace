from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Helpers for Home Assistant dispatcher & internal component/platform."""
import logging
from typing import Any, Callable

from homeassistant.core import callback
from homeassistant.loader import bind_hass
from homeassistant.util.async_ import run_callback_threadsafe
from .typing import HomeAssistantType


_LOGGER = logging.getLogger(__name__)
DATA_DISPATCHER = 'dispatcher'


@bind_hass
def __tmp6(hass, __tmp2,
                       __tmp0) :
    """Connect a callable function to a signal."""
    async_unsub = run_callback_threadsafe(
        hass.loop, __tmp5, hass, __tmp2, __tmp0).result()

    def __tmp3() :
        """Remove signal listener."""
        run_callback_threadsafe(hass.loop, async_unsub).result()

    return __tmp3


@callback
@bind_hass
def __tmp5(hass, __tmp2,
                             __tmp0) :
    """Connect a callable function to a signal.

    This method must be run in the event loop.
    """
    if DATA_DISPATCHER not in hass.data:
        hass.data[DATA_DISPATCHER] = {}

    if __tmp2 not in hass.data[DATA_DISPATCHER]:
        hass.data[DATA_DISPATCHER][__tmp2] = []

    hass.data[DATA_DISPATCHER][__tmp2].append(__tmp0)

    @callback
    def __tmp1() :
        """Remove signal listener."""
        try:
            hass.data[DATA_DISPATCHER][__tmp2].remove(__tmp0)
        except (KeyError, ValueError):
            # KeyError is key target listener did not exist
            # ValueError if listener did not exist within signal
            _LOGGER.warning(
                "Unable to remove unknown dispatcher %s", __tmp0)

    return __tmp1


@bind_hass
def __tmp7(hass, __tmp2, *args: <FILL>) :
    """Send signal and data."""
    hass.loop.call_soon_threadsafe(__tmp4, hass, __tmp2, *args)


@callback
@bind_hass
def __tmp4(
        hass, __tmp2, *args: Any) :
    """Send signal and data.

    This method must be run in the event loop.
    """
    target_list = hass.data.get(DATA_DISPATCHER, {}).get(__tmp2, [])

    for __tmp0 in target_list:
        hass.async_add_job(__tmp0, *args)
