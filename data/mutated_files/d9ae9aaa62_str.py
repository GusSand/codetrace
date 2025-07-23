from typing import TypeAlias
__typ1 : TypeAlias = "list"
__typ0 : TypeAlias = "int"
"""
Support for INSTEON fans via PowerLinc Modem.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/fan.insteon/
"""
import logging

from homeassistant.components.fan import (SPEED_OFF,
                                          SPEED_LOW,
                                          SPEED_MEDIUM,
                                          SPEED_HIGH,
                                          FanEntity,
                                          SUPPORT_SET_SPEED)
from homeassistant.const import STATE_OFF
from homeassistant.components.insteon import InsteonEntity

DEPENDENCIES = ['insteon']

SPEED_TO_HEX = {SPEED_OFF: 0x00,
                SPEED_LOW: 0x3f,
                SPEED_MEDIUM: 0xbe,
                SPEED_HIGH: 0xff}

FAN_SPEEDS = [STATE_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, __tmp1, async_add_entities,
                               discovery_info=None):
    """Set up the INSTEON device class for the hass platform."""
    insteon_modem = hass.data['insteon'].get('modem')

    address = discovery_info['address']
    device = insteon_modem.devices[address]
    state_key = discovery_info['state_key']

    _LOGGER.debug('Adding device %s entity %s to Fan platform',
                  device.address.hex, device.states[state_key].name)

    new_entity = InsteonFan(device, state_key)

    async_add_entities([new_entity])


class InsteonFan(InsteonEntity, FanEntity):
    """An INSTEON fan component."""

    @property
    def speed(__tmp0) -> str:
        """Return the current speed."""
        return __tmp0._hex_to_speed(__tmp0._insteon_device_state.value)

    @property
    def __tmp2(__tmp0) :
        """Get the list of available speeds."""
        return FAN_SPEEDS

    @property
    def supported_features(__tmp0) :
        """Flag supported features."""
        return SUPPORT_SET_SPEED

    async def async_turn_on(__tmp0, speed: str = None, **kwargs) :
        """Turn on the entity."""
        if speed is None:
            speed = SPEED_MEDIUM
        await __tmp0.async_set_speed(speed)

    async def async_turn_off(__tmp0, **kwargs) :
        """Turn off the entity."""
        await __tmp0.async_set_speed(SPEED_OFF)

    async def async_set_speed(__tmp0, speed: <FILL>) :
        """Set the speed of the fan."""
        fan_speed = SPEED_TO_HEX[speed]
        if fan_speed == 0x00:
            __tmp0._insteon_device_state.off()
        else:
            __tmp0._insteon_device_state.set_level(fan_speed)

    @staticmethod
    def _hex_to_speed(speed: __typ0):
        hex_speed = SPEED_OFF
        if speed > 0xfe:
            hex_speed = SPEED_HIGH
        elif speed > 0x7f:
            hex_speed = SPEED_MEDIUM
        elif speed > 0:
            hex_speed = SPEED_LOW
        return hex_speed
