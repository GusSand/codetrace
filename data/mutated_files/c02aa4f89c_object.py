"""
Support for Sesame, by CANDY HOUSE.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/lock.sesame/
"""
from typing import Callable
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.lock import LockDevice, PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_BATTERY_LEVEL, CONF_EMAIL, CONF_PASSWORD,
    STATE_LOCKED, STATE_UNLOCKED)
from homeassistant.helpers.typing import ConfigType

REQUIREMENTS = ['pysesame==0.1.0']

ATTR_DEVICE_ID = 'device_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(
        hass, config: ConfigType,
        add_entities: Callable[[list], None], discovery_info=None):
    """Set up the Sesame platform."""
    import pysesame

    email = config.get(CONF_EMAIL)
    password = config.get(CONF_PASSWORD)

    add_entities([__typ0(sesame) for sesame in
                  pysesame.get_sesames(email, password)],
                 update_before_add=True)


class __typ0(LockDevice):
    """Representation of a Sesame device."""

    def __init__(__tmp0, sesame: <FILL>) :
        """Initialize the Sesame device."""
        __tmp0._sesame = sesame

        # Cached properties from pysesame object.
        __tmp0._device_id = None
        __tmp0._nickname = None
        __tmp0._is_unlocked = False
        __tmp0._api_enabled = False
        __tmp0._battery = -1

    @property
    def name(__tmp0) :
        """Return the name of the device."""
        return __tmp0._nickname

    @property
    def available(__tmp0) -> bool:
        """Return True if entity is available."""
        return __tmp0._api_enabled

    @property
    def is_locked(__tmp0) -> bool:
        """Return True if the device is currently locked, else False."""
        return not __tmp0._is_unlocked

    @property
    def state(__tmp0) -> str:
        """Get the state of the device."""
        if __tmp0._is_unlocked:
            return STATE_UNLOCKED
        return STATE_LOCKED

    def lock(__tmp0, **kwargs) -> None:
        """Lock the device."""
        __tmp0._sesame.lock()

    def unlock(__tmp0, **kwargs) -> None:
        """Unlock the device."""
        __tmp0._sesame.unlock()

    def update(__tmp0) -> None:
        """Update the internal state of the device."""
        __tmp0._sesame.update_state()
        __tmp0._nickname = __tmp0._sesame.nickname
        __tmp0._api_enabled = __tmp0._sesame.api_enabled
        __tmp0._is_unlocked = __tmp0._sesame.is_unlocked
        __tmp0._device_id = __tmp0._sesame.device_id
        __tmp0._battery = __tmp0._sesame.battery

    @property
    def device_state_attributes(__tmp0) -> dict:
        """Return the state attributes."""
        attributes = {}
        attributes[ATTR_DEVICE_ID] = __tmp0._device_id
        attributes[ATTR_BATTERY_LEVEL] = __tmp0._battery
        return attributes
