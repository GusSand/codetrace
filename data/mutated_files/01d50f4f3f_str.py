from typing import TypeAlias
__typ1 : TypeAlias = "bool"
"""Config flow to configure SMHI component."""
import voluptuous as vol

from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client
import homeassistant.helpers.config_validation as cv
from homeassistant.util import slugify

from .const import DOMAIN, HOME_LOCATION_NAME


@callback
def __tmp0(hass: HomeAssistant):
    """Return configurations of SMHI component."""
    return set((slugify(entry.data[CONF_NAME])) for
               entry in hass.config_entries.async_entries(DOMAIN))


@config_entries.HANDLERS.register(DOMAIN)
class __typ0(data_entry_flow.FlowHandler):
    """Config flow for SMHI component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(__tmp1) -> None:
        """Initialize SMHI forecast configuration flow."""
        __tmp1._errors = {}

    async def __tmp2(__tmp1, user_input=None):
        """Handle a flow initialized by the user."""
        __tmp1._errors = {}

        if user_input is not None:
            is_ok = await __tmp1._check_location(
                user_input[CONF_LONGITUDE], user_input[CONF_LATITUDE])
            if is_ok:
                __tmp3 = slugify(user_input[CONF_NAME])
                if not __tmp1._name_in_configuration_exists(__tmp3):
                    return __tmp1.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input,
                    )

                __tmp1._errors[CONF_NAME] = 'name_exists'
            else:
                __tmp1._errors['base'] = 'wrong_location'

        # If hass config has the location set and is a valid coordinate the
        # default location is set as default values in the form
        if not __tmp0(__tmp1.hass):
            if await __tmp1._homeassistant_location_exists():
                return await __tmp1._show_config_form(
                    __tmp3=HOME_LOCATION_NAME,
                    latitude=__tmp1.hass.config.latitude,
                    longitude=__tmp1.hass.config.longitude
                )

        return await __tmp1._show_config_form()

    async def _homeassistant_location_exists(__tmp1) :
        """Return true if default location is set and is valid."""
        if __tmp1.hass.config.latitude != 0.0 and \
           __tmp1.hass.config.longitude != 0.0:
            # Return true if valid location
            if await __tmp1._check_location(
                    __tmp1.hass.config.longitude, __tmp1.hass.config.latitude):
                return True
        return False

    def _name_in_configuration_exists(__tmp1, __tmp3: str) -> __typ1:
        """Return True if name exists in configuration."""
        if __tmp3 in __tmp0(__tmp1.hass):
            return True
        return False

    async def _show_config_form(__tmp1, __tmp3: str = None, latitude: str = None,
                                longitude: str = None):
        """Show the configuration form to edit location data."""
        return __tmp1.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=__tmp3): str,
                vol.Required(CONF_LATITUDE, default=latitude): cv.latitude,
                vol.Required(CONF_LONGITUDE, default=longitude): cv.longitude
            }),
            errors=__tmp1._errors,
        )

    async def _check_location(__tmp1, longitude: <FILL>, latitude: str) -> __typ1:
        """Return true if location is ok."""
        from smhi.smhi_lib import Smhi, SmhiForecastException
        try:
            session = aiohttp_client.async_get_clientsession(__tmp1.hass)
            smhi_api = Smhi(longitude, latitude, session=session)

            await smhi_api.async_get_forecast()

            return True
        except SmhiForecastException:
            # The API will throw an exception if faulty location
            pass

        return False
