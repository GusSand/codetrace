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


def __tmp2(hass, __tmp7, add_entities, discovery_info=None):
    """Set up the Wink platform."""
    import pywink

    for fan in pywink.get_fans():
        if fan.object_id() + fan.name() not in hass.data[DOMAIN]['unique_ids']:
            add_entities([WinkFanDevice(fan, hass)])


class WinkFanDevice(WinkDevice, FanEntity):
    """Representation of a Wink fan."""

    async def __tmp1(__tmp0):
        """Call when entity is added to hass."""
        __tmp0.hass.data[DOMAIN]['entities']['fan'].append(__tmp0)

    def __tmp11(__tmp0, direction) :
        """Set the direction of the fan."""
        __tmp0.wink.set_fan_direction(direction)

    def __tmp3(__tmp0, __tmp6: <FILL>) :
        """Set the speed of the fan."""
        __tmp0.wink.set_state(True, __tmp6)

    def __tmp9(__tmp0, __tmp6: str = None, **kwargs) :
        """Turn on the fan."""
        __tmp0.wink.set_state(True, __tmp6)

    def __tmp5(__tmp0, **kwargs) :
        """Turn off the fan."""
        __tmp0.wink.set_state(False)

    @property
    def is_on(__tmp0):
        """Return true if the entity is on."""
        return __tmp0.wink.state()

    @property
    def __tmp6(__tmp0) :
        """Return the current speed."""
        current_wink_speed = __tmp0.wink.current_fan_speed()
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
    def __tmp4(__tmp0):
        """Return direction of the fan [forward, reverse]."""
        return __tmp0.wink.current_fan_direction()

    @property
    def __tmp8(__tmp0) :
        """Get the list of available speeds."""
        wink_supported_speeds = __tmp0.wink.fan_speeds()
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
    def __tmp10(__tmp0) :
        """Flag supported features."""
        return SUPPORTED_FEATURES
