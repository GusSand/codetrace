from typing import TypeAlias
__typ0 : TypeAlias = "State"
__typ2 : TypeAlias = "ConfigType"
__typ3 : TypeAlias = "bool"
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


async def async_setup_platform(hass, config: __typ2,
                               __tmp1,
                               discovery_info=None) -> None:
    """Initialize Light Switch platform."""
    __tmp1([__typ1(config.get(CONF_NAME),
                                    config[CONF_ENTITY_ID])], True)


class __typ1(Light):
    """Represents a Switch as a Light."""

    def __init__(__tmp3, name: str, __tmp2) :
        """Initialize Light Switch."""
        __tmp3._name = name  # type: str
        __tmp3._switch_entity_id = __tmp2  # type: str
        __tmp3._is_on = False  # type: bool
        __tmp3._available = False  # type: bool
        __tmp3._async_unsub_state_changed = None

    @property
    def name(__tmp3) -> str:
        """Return the name of the entity."""
        return __tmp3._name

    @property
    def is_on(__tmp3) -> __typ3:
        """Return true if light switch is on."""
        return __tmp3._is_on

    @property
    def available(__tmp3) -> __typ3:
        """Return true if light switch is on."""
        return __tmp3._available

    @property
    def should_poll(__tmp3) :
        """No polling needed for a light switch."""
        return False

    async def async_turn_on(__tmp3, **kwargs):
        """Forward the turn_on command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp3._switch_entity_id}
        await __tmp3.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_ON, data, blocking=True)

    async def async_turn_off(__tmp3, **kwargs):
        """Forward the turn_off command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp3._switch_entity_id}
        await __tmp3.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_OFF, data, blocking=True)

    async def async_update(__tmp3):
        """Query the switch in this light switch and determine the state."""
        switch_state = __tmp3.hass.states.get(__tmp3._switch_entity_id)

        if switch_state is None:
            __tmp3._available = False
            return

        __tmp3._is_on = switch_state.state == STATE_ON
        __tmp3._available = switch_state.state != STATE_UNAVAILABLE

    async def async_added_to_hass(__tmp3) :
        """Register callbacks."""
        @callback
        def async_state_changed_listener(__tmp0: <FILL>, old_state,
                                         new_state: __typ0):
            """Handle child updates."""
            __tmp3.async_schedule_update_ha_state(True)

        __tmp3._async_unsub_state_changed = async_track_state_change(
            __tmp3.hass, __tmp3._switch_entity_id, async_state_changed_listener)

    async def async_will_remove_from_hass(__tmp3):
        """Handle removal from Home Assistant."""
        if __tmp3._async_unsub_state_changed is not None:
            __tmp3._async_unsub_state_changed()
            __tmp3._async_unsub_state_changed = None
            __tmp3._available = False
