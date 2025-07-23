from typing import TypeAlias
__typ0 : TypeAlias = "State"
__typ4 : TypeAlias = "ConfigType"
__typ2 : TypeAlias = "HomeAssistantType"
__typ1 : TypeAlias = "bool"
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


async def async_setup_platform(hass: __typ2, config,
                               async_add_entities,
                               discovery_info=None) :
    """Initialize Light Switch platform."""
    async_add_entities([__typ3(config.get(CONF_NAME),
                                    config[CONF_ENTITY_ID])], True)


class __typ3(Light):
    """Represents a Switch as a Light."""

    def __init__(__tmp1, __tmp6: <FILL>, __tmp0: str) -> None:
        """Initialize Light Switch."""
        __tmp1._name = __tmp6  # type: str
        __tmp1._switch_entity_id = __tmp0  # type: str
        __tmp1._is_on = False  # type: bool
        __tmp1._available = False  # type: bool
        __tmp1._async_unsub_state_changed = None

    @property
    def __tmp6(__tmp1) -> str:
        """Return the name of the entity."""
        return __tmp1._name

    @property
    def is_on(__tmp1) -> __typ1:
        """Return true if light switch is on."""
        return __tmp1._is_on

    @property
    def __tmp3(__tmp1) -> __typ1:
        """Return true if light switch is on."""
        return __tmp1._available

    @property
    def should_poll(__tmp1) -> __typ1:
        """No polling needed for a light switch."""
        return False

    async def async_turn_on(__tmp1, **kwargs):
        """Forward the turn_on command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp1._switch_entity_id}
        await __tmp1.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_ON, data, blocking=True)

    async def __tmp5(__tmp1, **kwargs):
        """Forward the turn_off command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp1._switch_entity_id}
        await __tmp1.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_OFF, data, blocking=True)

    async def async_update(__tmp1):
        """Query the switch in this light switch and determine the state."""
        switch_state = __tmp1.hass.states.get(__tmp1._switch_entity_id)

        if switch_state is None:
            __tmp1._available = False
            return

        __tmp1._is_on = switch_state.state == STATE_ON
        __tmp1._available = switch_state.state != STATE_UNAVAILABLE

    async def async_added_to_hass(__tmp1) :
        """Register callbacks."""
        @callback
        def __tmp4(entity_id: str, old_state: __typ0,
                                         __tmp2: __typ0):
            """Handle child updates."""
            __tmp1.async_schedule_update_ha_state(True)

        __tmp1._async_unsub_state_changed = async_track_state_change(
            __tmp1.hass, __tmp1._switch_entity_id, __tmp4)

    async def async_will_remove_from_hass(__tmp1):
        """Handle removal from Home Assistant."""
        if __tmp1._async_unsub_state_changed is not None:
            __tmp1._async_unsub_state_changed()
            __tmp1._async_unsub_state_changed = None
            __tmp1._available = False
