from typing import TypeAlias
__typ1 : TypeAlias = "list"
"""
Support for Tuya fans.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/fan.tuya/
"""

from homeassistant.components.fan import (
    ENTITY_ID_FORMAT, FanEntity, SUPPORT_OSCILLATE, SUPPORT_SET_SPEED)
from homeassistant.components.tuya import DATA_TUYA, TuyaDevice
from homeassistant.const import STATE_OFF

DEPENDENCIES = ['tuya']


def __tmp2(hass, config, __tmp1, discovery_info=None):
    """Set up Tuya fan platform."""
    if discovery_info is None:
        return
    tuya = hass.data[DATA_TUYA]
    dev_ids = discovery_info.get('dev_ids')
    devices = []
    for dev_id in dev_ids:
        device = tuya.get_device_by_id(dev_id)
        if device is None:
            continue
        devices.append(__typ0(device))
    __tmp1(devices)


class __typ0(TuyaDevice, FanEntity):
    """Tuya fan devices."""

    def __init__(__tmp0, tuya):
        """Init Tuya fan device."""
        super().__init__(tuya)
        __tmp0.entity_id = ENTITY_ID_FORMAT.format(tuya.object_id())
        __tmp0.speeds = [STATE_OFF]

    async def async_added_to_hass(__tmp0):
        """Create fan list when add to hass."""
        await super().async_added_to_hass()
        __tmp0.speeds.extend(__tmp0.tuya.speed_list())

    def set_speed(__tmp0, speed: <FILL>) -> None:
        """Set the speed of the fan."""
        if speed == STATE_OFF:
            __tmp0.turn_off()
        else:
            __tmp0.tuya.set_speed(speed)

    def turn_on(__tmp0, speed: str = None, **kwargs) -> None:
        """Turn on the fan."""
        if speed is not None:
            __tmp0.set_speed(speed)
        else:
            __tmp0.tuya.turn_on()

    def turn_off(__tmp0, **kwargs) :
        """Turn the entity off."""
        __tmp0.tuya.turn_off()

    def oscillate(__tmp0, oscillating) -> None:
        """Oscillate the fan."""
        __tmp0.tuya.oscillate(oscillating)

    @property
    def oscillating(__tmp0):
        """Return current oscillating status."""
        if __tmp0.supported_features & SUPPORT_OSCILLATE == 0:
            return None
        if __tmp0.speed == STATE_OFF:
            return False
        return __tmp0.tuya.oscillating()

    @property
    def is_on(__tmp0):
        """Return true if the entity is on."""
        return __tmp0.tuya.state()

    @property
    def speed(__tmp0) -> str:
        """Return the current speed."""
        if __tmp0.is_on:
            return __tmp0.tuya.speed()
        return STATE_OFF

    @property
    def speed_list(__tmp0) -> __typ1:
        """Get the list of available speeds."""
        return __tmp0.speeds

    @property
    def supported_features(__tmp0) -> int:
        """Flag supported features."""
        supports = SUPPORT_SET_SPEED
        if __tmp0.tuya.support_oscillate():
            supports = supports | SUPPORT_OSCILLATE
        return supports
