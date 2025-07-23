from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""
Support for Sesame, by CANDY HOUSE.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/lock.sesame/
"""
from typing import Callable  # noqa
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


# pylint: disable=unused-argument
def setup_platform(hass, config,
                   add_devices, discovery_info=None):
    """Set up the Sesame platform."""
    import pysesame

    email = config.get(CONF_EMAIL)
    password = config.get(CONF_PASSWORD)

    add_devices([SesameDevice(sesame) for
                 sesame in pysesame.get_sesames(email, password)])


class SesameDevice(LockDevice):
    """Representation of a Sesame device."""

    _sesame = None

    def __init__(__tmp0, sesame: <FILL>) :
        """Initialize the Sesame device."""
        __tmp0._sesame = sesame

    @property
    def __tmp2(__tmp0) :
        """Return the name of the device."""
        return __tmp0._sesame.nickname

    @property
    def available(__tmp0) :
        """Return True if entity is available."""
        return __tmp0._sesame.api_enabled

    @property
    def is_locked(__tmp0) :
        """Return True if the device is currently locked, else False."""
        return not __tmp0._sesame.is_unlocked

    @property
    def __tmp1(__tmp0) -> __typ0:
        """Get the state of the device."""
        if __tmp0._sesame.is_unlocked:
            return STATE_UNLOCKED
        return STATE_LOCKED

    def lock(__tmp0, **kwargs) -> None:
        """Lock the device."""
        __tmp0._sesame.lock()

    def unlock(__tmp0, **kwargs) :
        """Unlock the device."""
        __tmp0._sesame.unlock()

    def update(__tmp0) :
        """Update the internal state of the device."""
        __tmp0._sesame.update_state()

    @property
    def device_state_attributes(__tmp0) :
        """Return the state attributes."""
        attributes = {}
        attributes[ATTR_DEVICE_ID] = __tmp0._sesame.device_id
        attributes[ATTR_BATTERY_LEVEL] = __tmp0._sesame.battery
        return attributes
