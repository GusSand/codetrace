from typing import TypeAlias
__typ0 : TypeAlias = "ConfigEntry"
"""Support for ESPHome fans."""
import logging
from typing import List, Optional, TYPE_CHECKING

from homeassistant.components.esphome import EsphomeEntity, \
    platform_async_setup_entry
from homeassistant.components.fan import FanEntity, SPEED_HIGH, SPEED_LOW, \
    SPEED_MEDIUM, SUPPORT_OSCILLATE, SUPPORT_SET_SPEED, SPEED_OFF
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from aioesphomeapi import FanInfo, FanState  # noqa

DEPENDENCIES = ['esphome']
_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(__tmp5,
                            entry, __tmp0) :
    """Set up ESPHome fans based on a config entry."""
    # pylint: disable=redefined-outer-name
    from aioesphomeapi import FanInfo, FanState  # noqa

    await platform_async_setup_entry(
        __tmp5, entry, __tmp0,
        component_key='fan',
        info_type=FanInfo, entity_type=EsphomeFan,
        state_type=FanState
    )


FAN_SPEED_STR_TO_INT = {
    SPEED_LOW: 0,
    SPEED_MEDIUM: 1,
    SPEED_HIGH: 2
}
FAN_SPEED_INT_TO_STR = {v: k for k, v in FAN_SPEED_STR_TO_INT.items()}


class EsphomeFan(EsphomeEntity, FanEntity):
    """A fan implementation for ESPHome."""

    @property
    def _static_info(__tmp1) :
        return super()._static_info

    @property
    def _state(__tmp1) :
        return super()._state

    async def __tmp3(__tmp1, speed: <FILL>) :
        """Set the speed of the fan."""
        if speed == SPEED_OFF:
            await __tmp1.async_turn_off()
            return
        await __tmp1._client.fan_command(
            __tmp1._static_info.key, speed=FAN_SPEED_STR_TO_INT[speed])

    async def __tmp4(__tmp1, speed: Optional[str] = None,
                            **kwargs) :
        """Turn on the fan."""
        if speed == SPEED_OFF:
            await __tmp1.async_turn_off()
            return
        data = {'key': __tmp1._static_info.key, 'state': True}
        if speed is not None:
            data['speed'] = FAN_SPEED_STR_TO_INT[speed]
        await __tmp1._client.fan_command(**data)

    # pylint: disable=arguments-differ
    async def async_turn_off(__tmp1, **kwargs) :
        """Turn off the fan."""
        await __tmp1._client.fan_command(key=__tmp1._static_info.key, state=False)

    async def __tmp6(__tmp1, oscillating):
        """Oscillate the fan."""
        await __tmp1._client.fan_command(key=__tmp1._static_info.key,
                                       oscillating=oscillating)

    @property
    def __tmp2(__tmp1) :
        """Return true if the entity is on."""
        if __tmp1._state is None:
            return None
        return __tmp1._state.state

    @property
    def speed(__tmp1) :
        """Return the current speed."""
        if __tmp1._state is None:
            return None
        if not __tmp1._static_info.supports_speed:
            return None
        return FAN_SPEED_INT_TO_STR[__tmp1._state.speed]

    @property
    def oscillating(__tmp1) :
        """Return the oscillation state."""
        if __tmp1._state is None:
            return None
        if not __tmp1._static_info.supports_oscillation:
            return None
        return __tmp1._state.oscillating

    @property
    def speed_list(__tmp1) :
        """Get the list of available speeds."""
        if not __tmp1._static_info.supports_speed:
            return None
        return [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    @property
    def supported_features(__tmp1) :
        """Flag supported features."""
        flags = 0
        if __tmp1._static_info.supports_oscillation:
            flags |= SUPPORT_OSCILLATE
        if __tmp1._static_info.supports_speed:
            flags |= SUPPORT_SET_SPEED
        return flags
