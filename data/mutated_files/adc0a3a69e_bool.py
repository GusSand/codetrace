from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "list"
__typ0 : TypeAlias = "int"
"""
Demo fan platform that has a fake fan.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
from homeassistant.components.fan import (SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH,
                                          FanEntity, SUPPORT_SET_SPEED,
                                          SUPPORT_OSCILLATE, SUPPORT_DIRECTION)
from homeassistant.const import STATE_OFF

FULL_SUPPORT = SUPPORT_SET_SPEED | SUPPORT_OSCILLATE | SUPPORT_DIRECTION
LIMITED_SUPPORT = SUPPORT_SET_SPEED


# pylint: disable=unused-argument
def setup_platform(hass, __tmp2, add_devices_callback, discovery_info=None):
    """Set up the demo fan platform."""
    add_devices_callback([
        __typ3(hass, "Living Room Fan", FULL_SUPPORT),
        __typ3(hass, "Ceiling Fan", LIMITED_SUPPORT),
    ])


class __typ3(FanEntity):
    """A demonstration fan component."""

    def __init__(__tmp0, hass, __tmp4, __tmp3) :
        """Initialize the entity."""
        __tmp0.hass = hass
        __tmp0._supported_features = __tmp3
        __tmp0._speed = STATE_OFF
        __tmp0.oscillating = None
        __tmp0.direction = None
        __tmp0._name = __tmp4

        if __tmp3 & SUPPORT_OSCILLATE:
            __tmp0.oscillating = False
        if __tmp3 & SUPPORT_DIRECTION:
            __tmp0.direction = "forward"

    @property
    def __tmp4(__tmp0) :
        """Get entity name."""
        return __tmp0._name

    @property
    def should_poll(__tmp0):
        """No polling needed for a demo fan."""
        return False

    @property
    def speed(__tmp0) :
        """Return the current speed."""
        return __tmp0._speed

    @property
    def speed_list(__tmp0) :
        """Get the list of available speeds."""
        return [STATE_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    def turn_on(__tmp0, speed: __typ1=None) :
        """Turn on the entity."""
        if speed is None:
            speed = SPEED_MEDIUM
        __tmp0.set_speed(speed)

    def turn_off(__tmp0) :
        """Turn off the entity."""
        __tmp0.oscillate(False)
        __tmp0.set_speed(STATE_OFF)

    def set_speed(__tmp0, speed) :
        """Set the speed of the fan."""
        __tmp0._speed = speed
        __tmp0.schedule_update_ha_state()

    def __tmp5(__tmp0, direction) :
        """Set the direction of the fan."""
        __tmp0.direction = direction
        __tmp0.schedule_update_ha_state()

    def oscillate(__tmp0, oscillating: <FILL>) :
        """Set oscillation."""
        __tmp0.oscillating = oscillating
        __tmp0.schedule_update_ha_state()

    @property
    def __tmp1(__tmp0) :
        """Fan direction."""
        return __tmp0.direction

    @property
    def __tmp3(__tmp0) :
        """Flag supported features."""
        return __tmp0._supported_features
