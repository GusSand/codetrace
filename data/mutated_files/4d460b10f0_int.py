from typing import TypeAlias
__typ0 : TypeAlias = "HomeAssistant"
__typ1 : TypeAlias = "FrameType"
"""Signal handling related helpers."""
import logging
import signal
import sys
from types import FrameType

from homeassistant.core import callback, HomeAssistant
from homeassistant.const import RESTART_EXIT_CODE
from homeassistant.loader import bind_hass

_LOGGER = logging.getLogger(__name__)


@callback
@bind_hass
def __tmp0(hass) :
    """Register system signal handler for core."""
    if sys.platform != 'win32':
        @callback
        def async_signal_handle(__tmp1: <FILL>) :
            """Wrap signal handling.

            * queue call to shutdown task
            * re-instate default handler
            """
            hass.loop.remove_signal_handler(signal.SIGTERM)
            hass.loop.remove_signal_handler(signal.SIGINT)
            hass.async_create_task(hass.async_stop(__tmp1))

        try:
            hass.loop.add_signal_handler(
                signal.SIGTERM, async_signal_handle, 0)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGTERM")

        try:
            hass.loop.add_signal_handler(
                signal.SIGINT, async_signal_handle, 0)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGINT")

        try:
            hass.loop.add_signal_handler(
                signal.SIGHUP, async_signal_handle, RESTART_EXIT_CODE)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGHUP")

    else:
        old_sigterm = None
        old_sigint = None

        @callback
        def async_signal_handle(__tmp1, __tmp2) :
            """Wrap signal handling.

            * queue call to shutdown task
            * re-instate default handler
            """
            signal.signal(signal.SIGTERM, old_sigterm)
            signal.signal(signal.SIGINT, old_sigint)
            hass.async_create_task(hass.async_stop(__tmp1))

        try:
            old_sigterm = signal.signal(signal.SIGTERM, async_signal_handle)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGTERM")

        try:
            old_sigint = signal.signal(signal.SIGINT, async_signal_handle)
        except ValueError:
            _LOGGER.warning("Could not bind to SIGINT")
