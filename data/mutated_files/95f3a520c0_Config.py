from typing import TypeAlias
__typ0 : TypeAlias = "ConfigEntry"
"""
Component for the Swedish weather institute weather service.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/smhi/
"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant

# Have to import for config_flow to work even if they are not used here
from .config_flow import smhi_locations  # noqa: F401
from .const import DOMAIN  # noqa: F401

REQUIREMENTS = ['smhi-pkg==1.0.5']

DEFAULT_NAME = 'smhi'


async def __tmp0(__tmp2, config: <FILL>) :
    """Set up configured SMHI."""
    # We allow setup only through config flow type of config
    return True


async def async_setup_entry(
        __tmp2, __tmp3) -> bool:
    """Set up SMHI forecast as config entry."""
    __tmp2.async_create_task(__tmp2.config_entries.async_forward_entry_setup(
        __tmp3, 'weather'))
    return True


async def __tmp1(
        __tmp2, __tmp3) -> bool:
    """Unload a config entry."""
    await __tmp2.config_entries.async_forward_entry_unload(
        __tmp3, 'weather')
    return True
