from typing import TypeAlias
__typ2 : TypeAlias = "list"
__typ0 : TypeAlias = "int"
"""
Support for Wink fans.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/fan.wink/
"""
import logging

from homeassistant.components.fan import (
    SPEED_HIGH, SPEED_LOW, SPEED_MEDIUM, STATE_UNKNOWN, SUPPORT_DIRECTION,
    SUPPORT_SET_SPEED, FanEntity)
from homeassistant.components.wink import DOMAIN, WinkDevice

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['wink']

SPEED_AUTO = 'auto'
SPEED_LOWEST = 'lowest'
SUPPORTED_FEATURES = SUPPORT_DIRECTION + SUPPORT_SET_SPEED


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Wink platform."""
    import pywink

    for fan in pywink.get_fans():
        if fan.object_id() + fan.name() not in hass.data[DOMAIN]['unique_ids']:
            add_entities([__typ1(fan, hass)])


class __typ1(WinkDevice, FanEntity):
    """Representation of a Wink fan."""

    async def __tmp2(__tmp1):
        """Call when entity is added to hass."""
        __tmp1.hass.data[DOMAIN]['entities']['fan'].append(__tmp1)

    def __tmp9(__tmp1, __tmp0: <FILL>) -> None:
        """Set the direction of the fan."""
        __tmp1.wink.set_fan_direction(__tmp0)

    def __tmp3(__tmp1, __tmp6) -> None:
        """Set the speed of the fan."""
        __tmp1.wink.set_state(True, __tmp6)

    def __tmp7(__tmp1, __tmp6: str = None, **kwargs) -> None:
        """Turn on the fan."""
        __tmp1.wink.set_state(True, __tmp6)

    def __tmp5(__tmp1, **kwargs) -> None:
        """Turn off the fan."""
        __tmp1.wink.set_state(False)

    @property
    def is_on(__tmp1):
        """Return true if the entity is on."""
        return __tmp1.wink.state()

    @property
    def __tmp6(__tmp1) :
        """Return the current speed."""
        current_wink_speed = __tmp1.wink.current_fan_speed()
        if SPEED_AUTO == current_wink_speed:
            return SPEED_AUTO
        if SPEED_LOWEST == current_wink_speed:
            return SPEED_LOWEST
        if SPEED_LOW == current_wink_speed:
            return SPEED_LOW
        if SPEED_MEDIUM == current_wink_speed:
            return SPEED_MEDIUM
        if SPEED_HIGH == current_wink_speed:
            return SPEED_HIGH
        return STATE_UNKNOWN

    @property
    def __tmp4(__tmp1):
        """Return direction of the fan [forward, reverse]."""
        return __tmp1.wink.current_fan_direction()

    @property
    def speed_list(__tmp1) :
        """Get the list of available speeds."""
        wink_supported_speeds = __tmp1.wink.fan_speeds()
        supported_speeds = []
        if SPEED_AUTO in wink_supported_speeds:
            supported_speeds.append(SPEED_AUTO)
        if SPEED_LOWEST in wink_supported_speeds:
            supported_speeds.append(SPEED_LOWEST)
        if SPEED_LOW in wink_supported_speeds:
            supported_speeds.append(SPEED_LOW)
        if SPEED_MEDIUM in wink_supported_speeds:
            supported_speeds.append(SPEED_MEDIUM)
        if SPEED_HIGH in wink_supported_speeds:
            supported_speeds.append(SPEED_HIGH)
        return supported_speeds

    @property
    def __tmp8(__tmp1) -> __typ0:
        """Flag supported features."""
        return SUPPORTED_FEATURES
