from typing import TypeAlias
__typ3 : TypeAlias = "float"
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "ConfigType"
"""
Support for ISY994 lights.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.isy994/
"""
import logging
from typing import Callable

from homeassistant.components.light import (
    Light, SUPPORT_BRIGHTNESS)
import homeassistant.components.isy994 as isy
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

UOM = ['2', '51', '78']
STATES = [STATE_OFF, STATE_ON, 'true', 'false', '%']


# pylint: disable=unused-argument
def setup_platform(__tmp0, config: __typ1,
                   __tmp2: Callable[[list], None], discovery_info=None):
    """Set up the ISY994 light platform."""
    if isy.ISY is None or not isy.ISY.connected:
        _LOGGER.error("A connection has not been made to the ISY controller")
        return False

    devices = []

    for __tmp3 in isy.filter_nodes(isy.NODES, units=UOM, states=STATES):
        if __tmp3.dimmable or '51' in __tmp3.uom:
            devices.append(__typ0(__tmp3))

    __tmp2(devices)


class __typ0(isy.ISYDevice, Light):
    """Representation of an ISY994 light devie."""

    def __init__(__tmp1, __tmp3: <FILL>) :
        """Initialize the ISY994 light device."""
        isy.ISYDevice.__init__(__tmp1, __tmp3)

    @property
    def is_on(__tmp1) -> __typ2:
        """Get whether the ISY994 light is on."""
        return __tmp1.value > 0

    @property
    def brightness(__tmp1) -> __typ3:
        """Get the brightness of the ISY994 light."""
        return __tmp1.value

    def turn_off(__tmp1, **kwargs) :
        """Send the turn off command to the ISY994 light device."""
        if not __tmp1._node.off():
            _LOGGER.debug("Unable to turn off light")

    def turn_on(__tmp1, brightness=None, **kwargs) -> None:
        """Send the turn on command to the ISY994 light device."""
        if not __tmp1._node.on(val=brightness):
            _LOGGER.debug("Unable to turn on light")

    @property
    def supported_features(__tmp1):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS
