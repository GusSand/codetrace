from typing import TypeAlias
__typ2 : TypeAlias = "ConfigType"
__typ3 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
"""
Light support for switch entities.

For more information about this platform, please refer to the documentation at
https://home-assistant.io/components/light.switch/
"""
import logging
import voluptuous as vol

from homeassistant.core import State, callback
from homeassistant.components.light import (
    Light, PLATFORM_SCHEMA)
from homeassistant.components import switch
from homeassistant.const import (
    STATE_ON,
    ATTR_ENTITY_ID,
    CONF_NAME,
    CONF_ENTITY_ID,
    STATE_UNAVAILABLE
)
from homeassistant.helpers.typing import HomeAssistantType, ConfigType
from homeassistant.helpers.event import async_track_state_change
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Light Switch'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_ENTITY_ID): cv.entity_domain(switch.DOMAIN)
})


async def __tmp12(hass: HomeAssistantType, config,
                               __tmp1,
                               discovery_info=None) -> None:
    """Initialize Light Switch platform."""
    __tmp1([__typ0(config.get(CONF_NAME),
                                    config[CONF_ENTITY_ID])], True)


class __typ0(Light):
    """Represents a Switch as a Light."""

    def __tmp10(__tmp3, __tmp15: __typ1, __tmp4: __typ1) -> None:
        """Initialize Light Switch."""
        __tmp3._name = __tmp15  # type: str
        __tmp3._switch_entity_id = __tmp4  # type: str
        __tmp3._is_on = False  # type: bool
        __tmp3._available = False  # type: bool
        __tmp3._async_unsub_state_changed = None

    @property
    def __tmp15(__tmp3) :
        """Return the name of the entity."""
        return __tmp3._name

    @property
    def is_on(__tmp3) :
        """Return true if light switch is on."""
        return __tmp3._is_on

    @property
    def __tmp7(__tmp3) :
        """Return true if light switch is on."""
        return __tmp3._available

    @property
    def __tmp16(__tmp3) -> __typ3:
        """No polling needed for a light switch."""
        return False

    async def __tmp13(__tmp3, **kwargs):
        """Forward the turn_on command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp3._switch_entity_id}
        await __tmp3.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_ON, data, blocking=True)

    async def __tmp11(__tmp3, **kwargs):
        """Forward the turn_off command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp3._switch_entity_id}
        await __tmp3.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_OFF, data, blocking=True)

    async def __tmp14(__tmp3):
        """Query the switch in this light switch and determine the state."""
        switch_state = __tmp3.hass.states.get(__tmp3._switch_entity_id)

        if switch_state is None:
            __tmp3._available = False
            return

        __tmp3._is_on = switch_state.state == STATE_ON
        __tmp3._available = switch_state.state != STATE_UNAVAILABLE

    async def __tmp5(__tmp3) -> None:
        """Register callbacks."""
        @callback
        def __tmp9(__tmp8: __typ1, __tmp0,
                                         __tmp6: <FILL>):
            """Handle child updates."""
            __tmp3.async_schedule_update_ha_state(True)

        __tmp3._async_unsub_state_changed = async_track_state_change(
            __tmp3.hass, __tmp3._switch_entity_id, __tmp9)

    async def __tmp2(__tmp3):
        """Handle removal from Home Assistant."""
        if __tmp3._async_unsub_state_changed is not None:
            __tmp3._async_unsub_state_changed()
            __tmp3._async_unsub_state_changed = None
            __tmp3._available = False
