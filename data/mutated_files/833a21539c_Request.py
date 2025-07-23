from typing import TypeAlias
__typ0 : TypeAlias = "Response"
"""
Support for Google Actions Smart Home Control.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/google_assistant/
"""
import logging

from aiohttp.web import Request, Response

# Typing imports
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import callback
from homeassistant.const import CLOUD_NEVER_EXPOSED_ENTITIES

from .const import (
    GOOGLE_ASSISTANT_API_ENDPOINT,
    CONF_ALLOW_UNLOCK,
    CONF_EXPOSE_BY_DEFAULT,
    CONF_EXPOSED_DOMAINS,
    CONF_ENTITY_CONFIG,
    CONF_EXPOSE,
    )
from .smart_home import async_handle_message
from .helpers import Config

_LOGGER = logging.getLogger(__name__)


@callback
def __tmp3(__tmp6, __tmp7):
    """Register HTTP views for Google Assistant."""
    expose_by_default = __tmp7.get(CONF_EXPOSE_BY_DEFAULT)
    exposed_domains = __tmp7.get(CONF_EXPOSED_DOMAINS)
    entity_config = __tmp7.get(CONF_ENTITY_CONFIG) or {}
    allow_unlock = __tmp7.get(CONF_ALLOW_UNLOCK, False)

    def is_exposed(__tmp5) :
        """Determine if an entity should be exposed to Google Assistant."""
        if __tmp5.attributes.get('view') is not None:
            # Ignore entities that are views
            return False

        if __tmp5.entity_id in CLOUD_NEVER_EXPOSED_ENTITIES:
            return False

        explicit_expose = \
            entity_config.get(__tmp5.entity_id, {}).get(CONF_EXPOSE)

        domain_exposed_by_default = \
            expose_by_default and __tmp5.domain in exposed_domains

        # Expose an entity if the entity's domain is exposed by default and
        # the configuration doesn't explicitly exclude it from being
        # exposed, or if the entity is explicitly exposed
        is_default_exposed = \
            domain_exposed_by_default and explicit_expose is not False

        return is_default_exposed or explicit_expose

    __tmp6.http.register_view(
        GoogleAssistantView(is_exposed, entity_config, allow_unlock))


class GoogleAssistantView(HomeAssistantView):
    """Handle Google Assistant requests."""

    url = GOOGLE_ASSISTANT_API_ENDPOINT
    name = 'api:google_assistant'
    requires_auth = True

    def __tmp4(__tmp0, is_exposed, entity_config, allow_unlock):
        """Initialize the Google Assistant request handler."""
        __tmp0.is_exposed = is_exposed
        __tmp0.entity_config = entity_config
        __tmp0.allow_unlock = allow_unlock

    async def __tmp1(__tmp0, __tmp2: <FILL>) :
        """Handle Google Assistant requests."""
        message = await __tmp2.json()  # type: dict
        config = Config(__tmp0.is_exposed,
                        __tmp0.allow_unlock,
                        __tmp2['hass_user'].id,
                        __tmp0.entity_config)
        result = await async_handle_message(
            __tmp2.app['hass'], config, message)
        return __tmp0.json(result)
