from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
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


def __tmp3(hass, __tmp2,
                   add_entities, discovery_info=None):
    """Set up the ISY994 cover platform."""
    devices = []
    for node in hass.data[ISY994_NODES][DOMAIN]:
        devices.append(ISYCoverDevice(node))

    for name, status, actions in hass.data[ISY994_PROGRAMS][DOMAIN]:
        devices.append(__typ0(name, status, actions))

    add_entities(devices)


class ISYCoverDevice(ISYDevice, CoverDevice):
    """Representation of an ISY994 cover device."""

    @property
    def current_cover_position(__tmp0) :
        """Return the current cover position."""
        if __tmp0.is_unknown() or __tmp0.value is None:
            return None
        return sorted((0, __tmp0.value, 100))[1]

    @property
    def is_closed(__tmp0) :
        """Get whether the ISY994 cover device is closed."""
        return __tmp0.state == STATE_CLOSED

    @property
    def state(__tmp0) :
        """Get the state of the ISY994 cover device."""
        if __tmp0.is_unknown():
            return None
        return VALUE_TO_STATE.get(__tmp0.value, STATE_OPEN)

    def __tmp1(__tmp0, **kwargs) :
        """Send the open cover command to the ISY994 cover device."""
        if not __tmp0._node.on(val=100):
            _LOGGER.error("Unable to open the cover")

    def close_cover(__tmp0, **kwargs) :
        """Send the close cover command to the ISY994 cover device."""
        if not __tmp0._node.off():
            _LOGGER.error("Unable to close the cover")


class __typ0(ISYCoverDevice):
    """Representation of an ISY994 cover program."""

    def __init__(__tmp0, name, node, actions: <FILL>) :
        """Initialize the ISY994 cover program."""
        super().__init__(node)
        __tmp0._name = name
        __tmp0._actions = actions

    @property
    def state(__tmp0) :
        """Get the state of the ISY994 cover program."""
        return STATE_CLOSED if __typ3(__tmp0.value) else STATE_OPEN

    def __tmp1(__tmp0, **kwargs) :
        """Send the open cover command to the ISY994 cover program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error("Unable to open the cover")

    def close_cover(__tmp0, **kwargs) :
        """Send the close cover command to the ISY994 cover program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error("Unable to close the cover")
