from typing import TypeAlias
__typ5 : TypeAlias = "ConfigType"
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "object"
__typ0 : TypeAlias = "int"
"""
Support for ISY994 covers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/cover.isy994/
"""
import logging
from typing import Callable

from homeassistant.components.cover import CoverDevice, DOMAIN
from homeassistant.components.isy994 import (ISY994_NODES, ISY994_PROGRAMS,
                                             ISYDevice)
from homeassistant.const import (
    STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING, STATE_UNKNOWN)
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

VALUE_TO_STATE = {
    0: STATE_CLOSED,
    101: STATE_UNKNOWN,
    102: 'stopped',
    103: STATE_CLOSING,
    104: STATE_OPENING
}


def setup_platform(hass, __tmp2: __typ5,
                   add_entities: Callable[[list], None], discovery_info=None):
    """Set up the ISY994 cover platform."""
    devices = []
    for node in hass.data[ISY994_NODES][DOMAIN]:
        devices.append(__typ1(node))

    for name, status, actions in hass.data[ISY994_PROGRAMS][DOMAIN]:
        devices.append(__typ4(name, status, actions))

    add_entities(devices)


class __typ1(ISYDevice, CoverDevice):
    """Representation of an ISY994 cover device."""

    @property
    def __tmp0(__tmp1) -> __typ0:
        """Return the current cover position."""
        if __tmp1.is_unknown() or __tmp1.value is None:
            return None
        return sorted((0, __tmp1.value, 100))[1]

    @property
    def is_closed(__tmp1) -> __typ2:
        """Get whether the ISY994 cover device is closed."""
        return __tmp1.state == STATE_CLOSED

    @property
    def state(__tmp1) -> str:
        """Get the state of the ISY994 cover device."""
        if __tmp1.is_unknown():
            return None
        return VALUE_TO_STATE.get(__tmp1.value, STATE_OPEN)

    def open_cover(__tmp1, **kwargs) -> None:
        """Send the open cover command to the ISY994 cover device."""
        if not __tmp1._node.on(val=100):
            _LOGGER.error("Unable to open the cover")

    def close_cover(__tmp1, **kwargs) -> None:
        """Send the close cover command to the ISY994 cover device."""
        if not __tmp1._node.off():
            _LOGGER.error("Unable to close the cover")


class __typ4(__typ1):
    """Representation of an ISY994 cover program."""

    def __init__(__tmp1, name: <FILL>, node: __typ3, actions: __typ3) :
        """Initialize the ISY994 cover program."""
        super().__init__(node)
        __tmp1._name = name
        __tmp1._actions = actions

    @property
    def state(__tmp1) -> str:
        """Get the state of the ISY994 cover program."""
        return STATE_CLOSED if __typ2(__tmp1.value) else STATE_OPEN

    def open_cover(__tmp1, **kwargs) -> None:
        """Send the open cover command to the ISY994 cover program."""
        if not __tmp1._actions.runThen():
            _LOGGER.error("Unable to open the cover")

    def close_cover(__tmp1, **kwargs) -> None:
        """Send the close cover command to the ISY994 cover program."""
        if not __tmp1._actions.runElse():
            _LOGGER.error("Unable to close the cover")
