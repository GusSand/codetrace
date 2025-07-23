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
def __tmp3(hass):
    """Return configurations of SMHI component."""
    return set((slugify(entry.data[CONF_NAME])) for
               entry in hass.config_entries.async_entries(DOMAIN))


@config_entries.HANDLERS.register(DOMAIN)
class __typ0(data_entry_flow.FlowHandler):
    """Config flow for SMHI component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __tmp1(__tmp0) :
        """Initialize SMHI forecast configuration flow."""
        __tmp0._errors = {}

    async def __tmp2(__tmp0, user_input=None):
        """Handle a flow initialized by the user."""
        __tmp0._errors = {}

        if user_input is not None:
            is_ok = await __tmp0._check_location(
                user_input[CONF_LONGITUDE], user_input[CONF_LATITUDE])
            if is_ok:
                __tmp4 = slugify(user_input[CONF_NAME])
                if not __tmp0._name_in_configuration_exists(__tmp4):
                    return __tmp0.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input,
                    )

                __tmp0._errors[CONF_NAME] = 'name_exists'
            else:
                __tmp0._errors['base'] = 'wrong_location'

        # If hass config has the location set and is a valid coordinate the
        # default location is set as default values in the form
        if not __tmp3(__tmp0.hass):
            if await __tmp0._homeassistant_location_exists():
                return await __tmp0._show_config_form(
                    __tmp4=HOME_LOCATION_NAME,
                    latitude=__tmp0.hass.config.latitude,
                    longitude=__tmp0.hass.config.longitude
                )

        return await __tmp0._show_config_form()

    async def _homeassistant_location_exists(__tmp0) :
        """Return true if default location is set and is valid."""
        if __tmp0.hass.config.latitude != 0.0 and \
           __tmp0.hass.config.longitude != 0.0:
            # Return true if valid location
            if await __tmp0._check_location(
                    __tmp0.hass.config.longitude, __tmp0.hass.config.latitude):
                return True
        return False

    def _name_in_configuration_exists(__tmp0, __tmp4: <FILL>) :
        """Return True if name exists in configuration."""
        if __tmp4 in __tmp3(__tmp0.hass):
            return True
        return False

    async def _show_config_form(__tmp0, __tmp4: str = None, latitude: str = None,
                                longitude: str = None):
        """Show the configuration form to edit location data."""
        return __tmp0.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=__tmp4): str,
                vol.Required(CONF_LATITUDE, default=latitude): cv.latitude,
                vol.Required(CONF_LONGITUDE, default=longitude): cv.longitude
            }),
            errors=__tmp0._errors,
        )

    async def _check_location(__tmp0, longitude, latitude) :
        """Return true if location is ok."""
        from smhi.smhi_lib import Smhi, SmhiForecastException
        try:
            session = aiohttp_client.async_get_clientsession(__tmp0.hass)
            smhi_api = Smhi(longitude, latitude, session=session)

            await smhi_api.async_get_forecast()

            return True
        except SmhiForecastException:
            # The API will throw an exception if faulty location
            pass

        return False
