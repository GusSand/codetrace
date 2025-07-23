from typing import TypeAlias
__typ0 : TypeAlias = "ToggleEntity"
"""
Support for Wink fans.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/fan.wink/
"""
import asyncio
import logging

from homeassistant.components.fan import (FanEntity, SPEED_HIGH,
                                          SPEED_LOW, SPEED_MEDIUM,
                                          STATE_UNKNOWN, SUPPORT_SET_SPEED,
                                          SUPPORT_DIRECTION)
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.components.wink import WinkDevice, DOMAIN

DEPENDENCIES = ['wink']

_LOGGER = logging.getLogger(__name__)

SPEED_LOWEST = 'lowest'
SPEED_AUTO = 'auto'

SUPPORTED_FEATURES = SUPPORT_DIRECTION + SUPPORT_SET_SPEED


def __tmp2(hass, config, add_devices, discovery_info=None):
    """Set up the Wink platform."""
    import pywink

    for fan in pywink.get_fans():
        if fan.object_id() + fan.name() not in hass.data[DOMAIN]['unique_ids']:
            add_devices([WinkFanDevice(fan, hass)])


class WinkFanDevice(WinkDevice, FanEntity):
    """Representation of a Wink fan."""

    @asyncio.coroutine
    def async_added_to_hass(__tmp1):
        """Callback when entity is added to hass."""
        __tmp1.hass.data[DOMAIN]['entities']['fan'].append(__tmp1)

    def set_direction(__tmp1, direction: str) :
        """Set the direction of the fan."""
        __tmp1.wink.set_fan_direction(direction)

    def set_speed(__tmp1: __typ0, speed: <FILL>) -> None:
        """Set the speed of the fan."""
        __tmp1.wink.set_state(True, speed)

    def turn_on(__tmp1: __typ0, speed: str=None, **kwargs) -> None:
        """Turn on the fan."""
        __tmp1.wink.set_state(True, speed)

    def turn_off(__tmp1: __typ0, **kwargs) -> None:
        """Turn off the fan."""
        __tmp1.wink.set_state(False)

    @property
    def is_on(__tmp1):
        """Return true if the entity is on."""
        return __tmp1.wink.state()

    @property
    def speed(__tmp1) -> str:
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
    def __tmp0(__tmp1):
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
    def supported_features(__tmp1: __typ0) -> int:
        """Flag supported features."""
        return SUPPORTED_FEATURES
