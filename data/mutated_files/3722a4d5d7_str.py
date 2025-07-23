from typing import TypeAlias
__typ0 : TypeAlias = "ConfigType"
"""
Support for ISY994 fans.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/fan.isy994/
"""
import logging
from typing import Callable

from homeassistant.components.fan import (FanEntity, DOMAIN, SPEED_OFF,
                                          SPEED_LOW, SPEED_MEDIUM,
                                          SPEED_HIGH)
import homeassistant.components.isy994 as isy
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

# Define term used for medium speed. This must be set as the fan component uses
# 'medium' which the ISY does not understand
ISY_SPEED_MEDIUM = 'med'


VALUE_TO_STATE = {
    0: SPEED_OFF,
    63: SPEED_LOW,
    64: SPEED_LOW,
    190: SPEED_MEDIUM,
    191: SPEED_MEDIUM,
    255: SPEED_HIGH,
}

STATE_TO_VALUE = {}
for key in VALUE_TO_STATE:
    STATE_TO_VALUE[VALUE_TO_STATE[key]] = key

STATES = [SPEED_OFF, SPEED_LOW, ISY_SPEED_MEDIUM, SPEED_HIGH]


# pylint: disable=unused-argument
def setup_platform(hass, config: __typ0,
                   add_devices: Callable[[list], None], discovery_info=None):
    """Set up the ISY994 fan platform."""
    if isy.ISY is None or not isy.ISY.connected:
        _LOGGER.error("A connection has not been made to the ISY controller")
        return False

    devices = []

    for node in isy.filter_nodes(isy.NODES, states=STATES):
        devices.append(ISYFanDevice(node))

    for program in isy.PROGRAMS.get(DOMAIN, []):
        try:
            status = program[isy.KEY_STATUS]
            actions = program[isy.KEY_ACTIONS]
            assert actions.dtype == 'program', 'Not a program'
        except (KeyError, AssertionError):
            pass
        else:
            devices.append(__typ1(program.name, status, actions))

    add_devices(devices)


class ISYFanDevice(isy.ISYDevice, FanEntity):
    """Representation of an ISY994 fan device."""

    def __init__(__tmp0, node) -> None:
        """Initialize the ISY994 fan device."""
        isy.ISYDevice.__init__(__tmp0, node)

    @property
    def speed(__tmp0) :
        """Return the current speed."""
        return VALUE_TO_STATE.get(__tmp0.value)

    @property
    def is_on(__tmp0) -> str:
        """Get if the fan is on."""
        return __tmp0.value != 0

    def set_speed(__tmp0, speed: str) -> None:
        """Send the set speed command to the ISY994 fan device."""
        __tmp0._node.on(val=STATE_TO_VALUE.get(speed, 255))

    def turn_on(__tmp0, speed: str=None, **kwargs) :
        """Send the turn on command to the ISY994 fan device."""
        __tmp0.set_speed(speed)

    def turn_off(__tmp0, **kwargs) -> None:
        """Send the turn off command to the ISY994 fan device."""
        __tmp0._node.off()

    @property
    def speed_list(__tmp0) -> list:
        """Get the list of available speeds."""
        return [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]


class __typ1(ISYFanDevice):
    """Representation of an ISY994 fan program."""

    def __init__(__tmp0, name: <FILL>, node, actions) -> None:
        """Initialize the ISY994 fan program."""
        ISYFanDevice.__init__(__tmp0, node)
        __tmp0._name = name
        __tmp0._actions = actions
        __tmp0.speed = STATE_ON if __tmp0.is_on else STATE_OFF

    @property
    def state(__tmp0) -> str:
        """Get the state of the ISY994 fan program."""
        return STATE_ON if bool(__tmp0.value) else STATE_OFF

    def turn_off(__tmp0, **kwargs) -> None:
        """Send the turn on command to ISY994 fan program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error("Unable to turn off the fan")
        else:
            __tmp0.speed = STATE_ON if __tmp0.is_on else STATE_OFF

    def turn_on(__tmp0, **kwargs) -> None:
        """Send the turn off command to ISY994 fan program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error("Unable to turn on the fan")
        else:
            __tmp0.speed = STATE_ON if __tmp0.is_on else STATE_OFF
