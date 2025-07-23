from typing import TypeAlias
__typ2 : TypeAlias = "object"
"""
Support for ISY994 covers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/cover.isy994/
"""
import logging
from typing import Callable  # noqa

from homeassistant.components.cover import CoverDevice, DOMAIN
import homeassistant.components.isy994 as isy
from homeassistant.const import STATE_OPEN, STATE_CLOSED, STATE_UNKNOWN
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

VALUE_TO_STATE = {
    0: STATE_CLOSED,
    101: STATE_UNKNOWN,
}

UOM = ['97']
STATES = [STATE_OPEN, STATE_CLOSED, 'closing', 'opening', 'stopped']


# pylint: disable=unused-argument
def setup_platform(hass, __tmp5,
                   add_devices, discovery_info=None):
    """Set up the ISY994 cover platform."""
    if isy.ISY is None or not isy.ISY.connected:
        _LOGGER.error("A connection has not been made to the ISY controller")
        return False

    devices = []

    for __tmp6 in isy.filter_nodes(isy.NODES, units=UOM, states=STATES):
        devices.append(__typ1(__tmp6))

    for program in isy.PROGRAMS.get(DOMAIN, []):
        try:
            status = program[isy.KEY_STATUS]
            __tmp1 = program[isy.KEY_ACTIONS]
            assert __tmp1.dtype == 'program', 'Not a program'
        except (KeyError, AssertionError):
            pass
        else:
            devices.append(__typ0(program.name, status, __tmp1))

    add_devices(devices)


class __typ1(isy.ISYDevice, CoverDevice):
    """Representation of an ISY994 cover device."""

    def __init__(__tmp0, __tmp6):
        """Initialize the ISY994 cover device."""
        isy.ISYDevice.__init__(__tmp0, __tmp6)

    @property
    def __tmp2(__tmp0) :
        """Return the current cover position."""
        return sorted((0, __tmp0.value, 100))[1]

    @property
    def __tmp4(__tmp0) :
        """Get whether the ISY994 cover device is closed."""
        return __tmp0.state == STATE_CLOSED

    @property
    def state(__tmp0) :
        """Get the state of the ISY994 cover device."""
        if __tmp0.is_unknown():
            return None
        else:
            return VALUE_TO_STATE.get(__tmp0.value, STATE_OPEN)

    def __tmp3(__tmp0, **kwargs) -> None:
        """Send the open cover command to the ISY994 cover device."""
        if not __tmp0._node.on(val=100):
            _LOGGER.error("Unable to open the cover")

    def __tmp7(__tmp0, **kwargs) -> None:
        """Send the close cover command to the ISY994 cover device."""
        if not __tmp0._node.off():
            _LOGGER.error("Unable to close the cover")


class __typ0(__typ1):
    """Representation of an ISY994 cover program."""

    def __init__(__tmp0, name: <FILL>, __tmp6, __tmp1: __typ2) :
        """Initialize the ISY994 cover program."""
        __typ1.__init__(__tmp0, __tmp6)
        __tmp0._name = name
        __tmp0._actions = __tmp1

    @property
    def state(__tmp0) :
        """Get the state of the ISY994 cover program."""
        return STATE_CLOSED if bool(__tmp0.value) else STATE_OPEN

    def __tmp3(__tmp0, **kwargs) -> None:
        """Send the open cover command to the ISY994 cover program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error("Unable to open the cover")

    def __tmp7(__tmp0, **kwargs) -> None:
        """Send the close cover command to the ISY994 cover program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error("Unable to close the cover")
