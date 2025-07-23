from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ3 : TypeAlias = "list"
__typ5 : TypeAlias = "ConfigType"
__typ1 : TypeAlias = "int"
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


def __tmp2(hass, __tmp7,
                   add_entities: Callable[[__typ3], None], discovery_info=None):
    """Set up the ISY994 fan platform."""
    devices = []

    for __tmp6 in hass.data[ISY994_NODES][DOMAIN]:
        devices.append(__typ0(__tmp6))

    for __tmp10, status, actions in hass.data[ISY994_PROGRAMS][DOMAIN]:
        devices.append(__typ2(__tmp10, status, actions))

    add_entities(devices)


class __typ0(ISYDevice, FanEntity):
    """Representation of an ISY994 fan device."""

    @property
    def __tmp4(__tmp0) -> str:
        """Return the current speed."""
        return VALUE_TO_STATE.get(__tmp0.value)

    @property
    def __tmp1(__tmp0) -> __typ4:
        """Get if the fan is on."""
        return __tmp0.value != 0

    def set_speed(__tmp0, __tmp4: <FILL>) -> None:
        """Send the set speed command to the ISY994 fan device."""
        __tmp0._node.on(val=STATE_TO_VALUE.get(__tmp4, 255))

    def __tmp8(__tmp0, __tmp4: str = None, **kwargs) -> None:
        """Send the turn on command to the ISY994 fan device."""
        __tmp0.set_speed(__tmp4)

    def __tmp3(__tmp0, **kwargs) -> None:
        """Send the turn off command to the ISY994 fan device."""
        __tmp0._node.off()

    @property
    def __tmp5(__tmp0) -> __typ3:
        """Get the list of available speeds."""
        return [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    @property
    def __tmp9(__tmp0) -> __typ1:
        """Flag supported features."""
        return SUPPORT_SET_SPEED


class __typ2(__typ0):
    """Representation of an ISY994 fan program."""

    def __init__(__tmp0, __tmp10: str, __tmp6, actions) -> None:
        """Initialize the ISY994 fan program."""
        super().__init__(__tmp6)
        __tmp0._name = __tmp10
        __tmp0._actions = actions

    def __tmp3(__tmp0, **kwargs) -> None:
        """Send the turn on command to ISY994 fan program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error("Unable to turn off the fan")

    def __tmp8(__tmp0, __tmp4: str = None, **kwargs) -> None:
        """Send the turn off command to ISY994 fan program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error("Unable to turn on the fan")

    @property
    def __tmp9(__tmp0) -> __typ1:
        """Flag supported features."""
        return 0
