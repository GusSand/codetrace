from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""
Support for ISY994 switches.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.isy994/
"""
import logging
from typing import Callable  # noqa

from homeassistant.components.switch import SwitchDevice, DOMAIN
import homeassistant.components.isy994 as isy
from homeassistant.const import STATE_ON, STATE_OFF, STATE_UNKNOWN
from homeassistant.helpers.typing import ConfigType  # noqa

_LOGGER = logging.getLogger(__name__)

VALUE_TO_STATE = {
    False: STATE_OFF,
    True: STATE_ON,
}

UOM = ['2', '78']
STATES = [STATE_OFF, STATE_ON, 'true', 'false']


# pylint: disable=unused-argument
def setup_platform(hass, __tmp2,
                   add_devices, discovery_info=None):
    """Set up the ISY994 switch platform."""
    if isy.ISY is None or not isy.ISY.connected:
        _LOGGER.error('A connection has not been made to the ISY controller.')
        return False

    devices = []

    for __tmp4 in isy.filter_nodes(isy.NODES, units=UOM,
                                 states=STATES):
        if not __tmp4.dimmable:
            devices.append(ISYSwitchDevice(__tmp4))

    for __tmp4 in isy.GROUPS:
        devices.append(ISYSwitchDevice(__tmp4))

    for program in isy.PROGRAMS.get(DOMAIN, []):
        try:
            status = program[isy.KEY_STATUS]
            actions = program[isy.KEY_ACTIONS]
            assert actions.dtype == 'program', 'Not a program'
        except (KeyError, AssertionError):
            pass
        else:
            devices.append(ISYSwitchProgram(program.name, status, actions))

    add_devices(devices)


class ISYSwitchDevice(isy.ISYDevice, SwitchDevice):
    """Representation of an ISY994 switch device."""

    def __init__(__tmp0, __tmp4) :
        """Initialize the ISY994 switch device."""
        isy.ISYDevice.__init__(__tmp0, __tmp4)

    @property
    def __tmp3(__tmp0) -> __typ0:
        """Get whether the ISY994 device is in the on state."""
        return __tmp0.state == STATE_ON

    @property
    def state(__tmp0) :
        """Get the state of the ISY994 device."""
        if __tmp0.is_unknown():
            return None
        else:
            return VALUE_TO_STATE.get(__typ0(__tmp0.value), STATE_UNKNOWN)

    def __tmp1(__tmp0, **kwargs) -> None:
        """Send the turn on command to the ISY994 switch."""
        if not __tmp0._node.off():
            _LOGGER.debug('Unable to turn on switch.')

    def turn_on(__tmp0, **kwargs) :
        """Send the turn off command to the ISY994 switch."""
        if not __tmp0._node.on():
            _LOGGER.debug('Unable to turn on switch.')


class ISYSwitchProgram(ISYSwitchDevice):
    """A representation of an ISY994 program switch."""

    def __init__(__tmp0, name: <FILL>, __tmp4, actions) :
        """Initialize the ISY994 switch program."""
        ISYSwitchDevice.__init__(__tmp0, __tmp4)
        __tmp0._name = name
        __tmp0._actions = actions

    @property
    def __tmp3(__tmp0) :
        """Get whether the ISY994 switch program is on."""
        return __typ0(__tmp0.value)

    def turn_on(__tmp0, **kwargs) :
        """Send the turn on command to the ISY994 switch program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error('Unable to turn on switch')

    def __tmp1(__tmp0, **kwargs) :
        """Send the turn off command to the ISY994 switch program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error('Unable to turn off switch')
