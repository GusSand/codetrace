from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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


async def async_setup_platform(hass, config: ConfigType,
                               async_add_entities,
                               discovery_info=None) -> None:
    """Initialize Light Switch platform."""
    async_add_entities([LightSwitch(config.get(CONF_NAME),
                                    config[CONF_ENTITY_ID])], True)


class LightSwitch(Light):
    """Represents a Switch as a Light."""

    def __init__(__tmp2, __tmp3: str, switch_entity_id: <FILL>) :
        """Initialize Light Switch."""
        __tmp2._name = __tmp3  # type: str
        __tmp2._switch_entity_id = switch_entity_id  # type: str
        __tmp2._is_on = False  # type: bool
        __tmp2._available = False  # type: bool
        __tmp2._async_unsub_state_changed = None

    @property
    def __tmp3(__tmp2) :
        """Return the name of the entity."""
        return __tmp2._name

    @property
    def is_on(__tmp2) :
        """Return true if light switch is on."""
        return __tmp2._is_on

    @property
    def available(__tmp2) -> __typ0:
        """Return true if light switch is on."""
        return __tmp2._available

    @property
    def should_poll(__tmp2) -> __typ0:
        """No polling needed for a light switch."""
        return False

    async def async_turn_on(__tmp2, **kwargs):
        """Forward the turn_on command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp2._switch_entity_id}
        await __tmp2.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_ON, data, blocking=True)

    async def async_turn_off(__tmp2, **kwargs):
        """Forward the turn_off command to the switch in this light switch."""
        data = {ATTR_ENTITY_ID: __tmp2._switch_entity_id}
        await __tmp2.hass.services.async_call(
            switch.DOMAIN, switch.SERVICE_TURN_OFF, data, blocking=True)

    async def async_update(__tmp2):
        """Query the switch in this light switch and determine the state."""
        switch_state = __tmp2.hass.states.get(__tmp2._switch_entity_id)

        if switch_state is None:
            __tmp2._available = False
            return

        __tmp2._is_on = switch_state.state == STATE_ON
        __tmp2._available = switch_state.state != STATE_UNAVAILABLE

    async def async_added_to_hass(__tmp2) :
        """Register callbacks."""
        @callback
        def async_state_changed_listener(__tmp1, __tmp0: State,
                                         new_state: State):
            """Handle child updates."""
            __tmp2.async_schedule_update_ha_state(True)

        __tmp2._async_unsub_state_changed = async_track_state_change(
            __tmp2.hass, __tmp2._switch_entity_id, async_state_changed_listener)

    async def async_will_remove_from_hass(__tmp2):
        """Handle removal from Home Assistant."""
        if __tmp2._async_unsub_state_changed is not None:
            __tmp2._async_unsub_state_changed()
            __tmp2._async_unsub_state_changed = None
            __tmp2._available = False
