from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
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
def setup_platform(hass, __tmp4,
                   __tmp2: Callable[[list], None], discovery_info=None):
    """Set up the ISY994 cover platform."""
    if isy.ISY is None or not isy.ISY.connected:
        _LOGGER.error("A connection has not been made to the ISY controller")
        return False

    devices = []

    for __tmp5 in isy.filter_nodes(isy.NODES, units=UOM, states=STATES):
        devices.append(__typ2(__tmp5))

    for program in isy.PROGRAMS.get(DOMAIN, []):
        try:
            status = program[isy.KEY_STATUS]
            actions = program[isy.KEY_ACTIONS]
            assert actions.dtype == 'program', 'Not a program'
        except (KeyError, AssertionError):
            pass
        else:
            devices.append(__typ4(program.name, status, actions))

    __tmp2(devices)


class __typ2(isy.ISYDevice, CoverDevice):
    """Representation of an ISY994 cover device."""

    def __init__(__tmp0, __tmp5):
        """Initialize the ISY994 cover device."""
        isy.ISYDevice.__init__(__tmp0, __tmp5)

    @property
    def __tmp1(__tmp0) -> __typ0:
        """Return the current cover position."""
        return sorted((0, __tmp0.value, 100))[1]

    @property
    def __tmp3(__tmp0) :
        """Get whether the ISY994 cover device is closed."""
        return __tmp0.state == STATE_CLOSED

    @property
    def state(__tmp0) -> __typ1:
        """Get the state of the ISY994 cover device."""
        if __tmp0.is_unknown():
            return None
        else:
            return VALUE_TO_STATE.get(__tmp0.value, STATE_OPEN)

    def open_cover(__tmp0, **kwargs) -> None:
        """Send the open cover command to the ISY994 cover device."""
        if not __tmp0._node.on(val=100):
            _LOGGER.error("Unable to open the cover")

    def __tmp6(__tmp0, **kwargs) -> None:
        """Send the close cover command to the ISY994 cover device."""
        if not __tmp0._node.off():
            _LOGGER.error("Unable to close the cover")


class __typ4(__typ2):
    """Representation of an ISY994 cover program."""

    def __init__(__tmp0, name: __typ1, __tmp5: <FILL>, actions: object) :
        """Initialize the ISY994 cover program."""
        __typ2.__init__(__tmp0, __tmp5)
        __tmp0._name = name
        __tmp0._actions = actions

    @property
    def state(__tmp0) -> __typ1:
        """Get the state of the ISY994 cover program."""
        return STATE_CLOSED if __typ3(__tmp0.value) else STATE_OPEN

    def open_cover(__tmp0, **kwargs) :
        """Send the open cover command to the ISY994 cover program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error("Unable to open the cover")

    def __tmp6(__tmp0, **kwargs) :
        """Send the close cover command to the ISY994 cover program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error("Unable to close the cover")
