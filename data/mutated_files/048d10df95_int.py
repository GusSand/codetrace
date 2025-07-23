from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def setup_platform(hass, config, add_entities_callback, discovery_info=None):
    """Set up the demo fan platform."""
    add_entities_callback([
        __typ1(hass, "Living Room Fan", FULL_SUPPORT),
        __typ1(hass, "Ceiling Fan", LIMITED_SUPPORT),
    ])


class __typ1(FanEntity):
    """A demonstration fan component."""

    def __init__(__tmp2, hass, __tmp3, supported_features: <FILL>) :
        """Initialize the entity."""
        __tmp2.hass = hass
        __tmp2._supported_features = supported_features
        __tmp2._speed = STATE_OFF
        __tmp2.oscillating = None
        __tmp2.direction = None
        __tmp2._name = __tmp3

        if supported_features & SUPPORT_OSCILLATE:
            __tmp2.oscillating = False
        if supported_features & SUPPORT_DIRECTION:
            __tmp2.direction = "forward"

    @property
    def __tmp3(__tmp2) :
        """Get entity name."""
        return __tmp2._name

    @property
    def should_poll(__tmp2):
        """No polling needed for a demo fan."""
        return False

    @property
    def speed(__tmp2) -> __typ0:
        """Return the current speed."""
        return __tmp2._speed

    @property
    def speed_list(__tmp2) -> list:
        """Get the list of available speeds."""
        return [STATE_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    def turn_on(__tmp2, speed: __typ0 = None, **kwargs) :
        """Turn on the entity."""
        if speed is None:
            speed = SPEED_MEDIUM
        __tmp2.set_speed(speed)

    def __tmp1(__tmp2, **kwargs) :
        """Turn off the entity."""
        __tmp2.oscillate(False)
        __tmp2.set_speed(STATE_OFF)

    def set_speed(__tmp2, speed) :
        """Set the speed of the fan."""
        __tmp2._speed = speed
        __tmp2.schedule_update_ha_state()

    def set_direction(__tmp2, direction) :
        """Set the direction of the fan."""
        __tmp2.direction = direction
        __tmp2.schedule_update_ha_state()

    def oscillate(__tmp2, oscillating) -> None:
        """Set oscillation."""
        __tmp2.oscillating = oscillating
        __tmp2.schedule_update_ha_state()

    @property
    def __tmp0(__tmp2) :
        """Fan direction."""
        return __tmp2.direction

    @property
    def supported_features(__tmp2) :
        """Flag supported features."""
        return __tmp2._supported_features
