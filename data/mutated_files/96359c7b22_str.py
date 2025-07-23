from typing import TypeAlias
__typ1 : TypeAlias = "bool"
"""
Support for ISY994 switches.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.isy994/
"""
import logging
from typing import Callable

from homeassistant.components.switch import SwitchDevice, DOMAIN
from homeassistant.components.isy994 import (ISY994_NODES, ISY994_PROGRAMS,
                                             ISYDevice)
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)


def __tmp1(hass, __tmp2: ConfigType,
                   add_entities: Callable[[list], None], discovery_info=None):
    """Set up the ISY994 switch platform."""
    devices = []
    for node in hass.data[ISY994_NODES][DOMAIN]:
        if not node.dimmable:
            devices.append(__typ0(node))

    for name, status, actions in hass.data[ISY994_PROGRAMS][DOMAIN]:
        devices.append(ISYSwitchProgram(name, status, actions))

    add_entities(devices)


class __typ0(ISYDevice, SwitchDevice):
    """Representation of an ISY994 switch device."""

    @property
    def __tmp4(__tmp0) :
        """Get whether the ISY994 device is in the on state."""
        return __typ1(__tmp0.value)

    def turn_off(__tmp0, **kwargs) :
        """Send the turn on command to the ISY994 switch."""
        if not __tmp0._node.off():
            _LOGGER.debug('Unable to turn on switch.')

    def __tmp3(__tmp0, **kwargs) -> None:
        """Send the turn off command to the ISY994 switch."""
        if not __tmp0._node.on():
            _LOGGER.debug('Unable to turn on switch.')


class ISYSwitchProgram(__typ0):
    """A representation of an ISY994 program switch."""

    def __init__(__tmp0, name: <FILL>, node, actions) -> None:
        """Initialize the ISY994 switch program."""
        super().__init__(node)
        __tmp0._name = name
        __tmp0._actions = actions

    @property
    def __tmp4(__tmp0) -> __typ1:
        """Get whether the ISY994 switch program is on."""
        return __typ1(__tmp0.value)

    def __tmp3(__tmp0, **kwargs) :
        """Send the turn on command to the ISY994 switch program."""
        if not __tmp0._actions.runThen():
            _LOGGER.error('Unable to turn on switch')

    def turn_off(__tmp0, **kwargs) :
        """Send the turn off command to the ISY994 switch program."""
        if not __tmp0._actions.runElse():
            _LOGGER.error('Unable to turn off switch')
