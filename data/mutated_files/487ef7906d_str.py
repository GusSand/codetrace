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


def setup_platform(hass, config, __tmp2, discovery_info=None):
    """Set up the demo fan platform."""
    __tmp2([
        __typ0(hass, "Living Room Fan", FULL_SUPPORT),
        __typ0(hass, "Ceiling Fan", LIMITED_SUPPORT),
    ])


class __typ0(FanEntity):
    """A demonstration fan component."""

    def __init__(__tmp1, hass, name, supported_features) :
        """Initialize the entity."""
        __tmp1.hass = hass
        __tmp1._supported_features = supported_features
        __tmp1._speed = STATE_OFF
        __tmp1.oscillating = None
        __tmp1.direction = None
        __tmp1._name = name

        if supported_features & SUPPORT_OSCILLATE:
            __tmp1.oscillating = False
        if supported_features & SUPPORT_DIRECTION:
            __tmp1.direction = "forward"

    @property
    def name(__tmp1) :
        """Get entity name."""
        return __tmp1._name

    @property
    def should_poll(__tmp1):
        """No polling needed for a demo fan."""
        return False

    @property
    def speed(__tmp1) :
        """Return the current speed."""
        return __tmp1._speed

    @property
    def speed_list(__tmp1) :
        """Get the list of available speeds."""
        return [STATE_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    def turn_on(__tmp1, speed: str = None, **kwargs) :
        """Turn on the entity."""
        if speed is None:
            speed = SPEED_MEDIUM
        __tmp1.set_speed(speed)

    def turn_off(__tmp1, **kwargs) :
        """Turn off the entity."""
        __tmp1.oscillate(False)
        __tmp1.set_speed(STATE_OFF)

    def set_speed(__tmp1, speed: <FILL>) :
        """Set the speed of the fan."""
        __tmp1._speed = speed
        __tmp1.schedule_update_ha_state()

    def set_direction(__tmp1, direction) -> None:
        """Set the direction of the fan."""
        __tmp1.direction = direction
        __tmp1.schedule_update_ha_state()

    def oscillate(__tmp1, oscillating) :
        """Set oscillation."""
        __tmp1.oscillating = oscillating
        __tmp1.schedule_update_ha_state()

    @property
    def __tmp0(__tmp1) -> str:
        """Fan direction."""
        return __tmp1.direction

    @property
    def supported_features(__tmp1) :
        """Flag supported features."""
        return __tmp1._supported_features
