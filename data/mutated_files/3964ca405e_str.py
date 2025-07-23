from typing import TypeAlias
__typ0 : TypeAlias = "list"
"""
Support for ISY994 fans.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/fan.isy994/
"""
import logging
from typing import Callable

from homeassistant.components.fan import (FanEntity, DOMAIN, SPEED_OFF,
                                          SPEED_LOW, SPEED_MEDIUM,
                                          SPEED_HIGH, SUPPORT_SET_SPEED)
from homeassistant.components.isy994 import (ISY994_NODES, ISY994_PROGRAMS,
                                             ISYDevice)
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

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


def setup_platform(hass, config,
                   add_entities, discovery_info=None):
    """Set up the ISY994 fan platform."""
    devices = []

    for node in hass.data[ISY994_NODES][DOMAIN]:
        devices.append(ISYFanDevice(node))

    for name, status, actions in hass.data[ISY994_PROGRAMS][DOMAIN]:
        devices.append(__typ1(name, status, actions))

    add_entities(devices)


class ISYFanDevice(ISYDevice, FanEntity):
    """Representation of an ISY994 fan device."""

    @property
    def speed(__tmp1) :
        """Return the current speed."""
        return VALUE_TO_STATE.get(__tmp1.value)

    @property
    def is_on(__tmp1) :
        """Get if the fan is on."""
        return __tmp1.value != 0

    def set_speed(__tmp1, speed) :
        """Send the set speed command to the ISY994 fan device."""
        __tmp1._node.on(val=STATE_TO_VALUE.get(speed, 255))

    def turn_on(__tmp1, speed: str = None, **kwargs) :
        """Send the turn on command to the ISY994 fan device."""
        __tmp1.set_speed(speed)

    def __tmp0(__tmp1, **kwargs) :
        """Send the turn off command to the ISY994 fan device."""
        __tmp1._node.off()

    @property
    def speed_list(__tmp1) :
        """Get the list of available speeds."""
        return [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    @property
    def supported_features(__tmp1) :
        """Flag supported features."""
        return SUPPORT_SET_SPEED


class __typ1(ISYFanDevice):
    """Representation of an ISY994 fan program."""

    def __init__(__tmp1, name: <FILL>, node, actions) :
        """Initialize the ISY994 fan program."""
        super().__init__(node)
        __tmp1._name = name
        __tmp1._actions = actions

    def __tmp0(__tmp1, **kwargs) :
        """Send the turn on command to ISY994 fan program."""
        if not __tmp1._actions.runThen():
            _LOGGER.error("Unable to turn off the fan")

    def turn_on(__tmp1, speed: str = None, **kwargs) :
        """Send the turn off command to ISY994 fan program."""
        if not __tmp1._actions.runElse():
            _LOGGER.error("Unable to turn on the fan")

    @property
    def supported_features(__tmp1) :
        """Flag supported features."""
        return 0
