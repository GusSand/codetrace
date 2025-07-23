from typing import TypeAlias
__typ1 : TypeAlias = "HomeAssistantType"
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
def __tmp3(hass, __tmp2: __typ0,
                       __tmp1: Callable[..., None]) -> Callable[[], None]:
    """Connect a callable function to a signal."""
    async_unsub = run_callback_threadsafe(
        hass.loop, async_dispatcher_connect, hass, __tmp2, __tmp1).result()

    def remove_dispatcher() -> None:
        """Remove signal listener."""
        run_callback_threadsafe(hass.loop, async_unsub).result()

    return remove_dispatcher


@callback
@bind_hass
def async_dispatcher_connect(hass: __typ1, __tmp2: __typ0,
                             __tmp1: Callable[..., Any]) :
    """Connect a callable function to a signal.

    This method must be run in the event loop.
    """
    if DATA_DISPATCHER not in hass.data:
        hass.data[DATA_DISPATCHER] = {}

    if __tmp2 not in hass.data[DATA_DISPATCHER]:
        hass.data[DATA_DISPATCHER][__tmp2] = []

    hass.data[DATA_DISPATCHER][__tmp2].append(__tmp1)

    @callback
    def async_remove_dispatcher() :
        """Remove signal listener."""
        try:
            hass.data[DATA_DISPATCHER][__tmp2].remove(__tmp1)
        except (KeyError, ValueError):
            # KeyError is key target listener did not exist
            # ValueError if listener did not exist within signal
            _LOGGER.warning(
                "Unable to remove unknown dispatcher %s", __tmp1)

    return async_remove_dispatcher


@bind_hass
def dispatcher_send(hass: __typ1, __tmp2: __typ0, *args: Any) :
    """Send signal and data."""
    hass.loop.call_soon_threadsafe(__tmp0, hass, __tmp2, *args)


@callback
@bind_hass
def __tmp0(
        hass: __typ1, __tmp2: __typ0, *args: <FILL>) -> None:
    """Send signal and data.

    This method must be run in the event loop.
    """
    target_list = hass.data.get(DATA_DISPATCHER, {}).get(__tmp2, [])

    for __tmp1 in target_list:
        hass.async_add_job(__tmp1, *args)
