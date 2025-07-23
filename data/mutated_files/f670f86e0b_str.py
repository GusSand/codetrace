"""
Support for switch devices that can be controlled using the RaspyRFM rc module.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.raspyrfm/
"""
import logging

import voluptuous as vol

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice
from homeassistant.const import (
    CONF_HOST, CONF_NAME, CONF_PORT, CONF_SWITCHES,
    DEVICE_DEFAULT_NAME)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['raspyrfm-client==1.2.8']
_LOGGER = logging.getLogger(__name__)

CONF_GATEWAY_MANUFACTURER = 'gateway_manufacturer'
CONF_GATEWAY_MODEL = 'gateway_model'
CONF_CONTROLUNIT_MANUFACTURER = 'controlunit_manufacturer'
CONF_CONTROLUNIT_MODEL = 'controlunit_model'
CONF_CHANNEL_CONFIG = 'channel_config'
DEFAULT_HOST = '127.0.0.1'

# define configuration parameters
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_PORT): cv.port,
    vol.Optional(CONF_GATEWAY_MANUFACTURER): cv.string,
    vol.Optional(CONF_GATEWAY_MODEL): cv.string,
    vol.Required(CONF_SWITCHES): vol.Schema([{
        vol.Optional(CONF_NAME, default=DEVICE_DEFAULT_NAME): cv.string,
        vol.Required(CONF_CONTROLUNIT_MANUFACTURER): cv.string,
        vol.Required(CONF_CONTROLUNIT_MODEL): cv.string,
        vol.Required(CONF_CHANNEL_CONFIG): {cv.string: cv.match_all},
    }])
}, extra=vol.ALLOW_EXTRA)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the RaspyRFM switch."""
    from raspyrfm_client import RaspyRFMClient
    from raspyrfm_client.device_implementations.controlunit. \
        controlunit_constants import ControlUnitModel
    from raspyrfm_client.device_implementations.gateway.manufacturer. \
        gateway_constants import GatewayModel
    from raspyrfm_client.device_implementations.manufacturer_constants \
        import Manufacturer

    gateway_manufacturer = config.get(CONF_GATEWAY_MANUFACTURER,
                                      Manufacturer.SEEGEL_SYSTEME.value)
    gateway_model = config.get(CONF_GATEWAY_MODEL, GatewayModel.RASPYRFM.value)
    host = config[CONF_HOST]
    port = config.get(CONF_PORT)
    switches = config[CONF_SWITCHES]

    raspyrfm_client = RaspyRFMClient()
    gateway = raspyrfm_client.get_gateway(Manufacturer(gateway_manufacturer),
                                          GatewayModel(gateway_model), host,
                                          port)
    switch_entities = []
    for switch in switches:
        name = switch[CONF_NAME]
        controlunit_manufacturer = switch[CONF_CONTROLUNIT_MANUFACTURER]
        controlunit_model = switch[CONF_CONTROLUNIT_MODEL]
        channel_config = switch[CONF_CHANNEL_CONFIG]

        controlunit = raspyrfm_client.get_controlunit(
            Manufacturer(controlunit_manufacturer),
            ControlUnitModel(controlunit_model))

        controlunit.set_channel_config(**channel_config)

        switch = __typ0(raspyrfm_client, name, gateway, controlunit)
        switch_entities.append(switch)

    add_entities(switch_entities)


class __typ0(SwitchDevice):
    """Representation of a RaspyRFM switch."""

    def __init__(__tmp1, raspyrfm_client, name: <FILL>, gateway, controlunit):
        """Initialize the switch."""
        __tmp1._raspyrfm_client = raspyrfm_client

        __tmp1._name = name
        __tmp1._gateway = gateway
        __tmp1._controlunit = controlunit

        __tmp1._state = None

    @property
    def name(__tmp1):
        """Return the name of the device if any."""
        return __tmp1._name

    @property
    def should_poll(__tmp1):
        """Return True if polling should be used."""
        return False

    @property
    def assumed_state(__tmp1):
        """Return True when the current state can not be queried."""
        return True

    @property
    def is_on(__tmp1):
        """Return true if switch is on."""
        return __tmp1._state

    def turn_on(__tmp1, **kwargs):
        """Turn the switch on."""
        from raspyrfm_client.device_implementations.controlunit.actions \
            import Action

        __tmp1._raspyrfm_client.send(__tmp1._gateway, __tmp1._controlunit, Action.ON)
        __tmp1._state = True
        __tmp1.schedule_update_ha_state()

    def __tmp0(__tmp1, **kwargs):
        """Turn the switch off."""
        from raspyrfm_client.device_implementations.controlunit.actions \
            import Action

        if Action.OFF in __tmp1._controlunit.get_supported_actions():
            __tmp1._raspyrfm_client.send(
                __tmp1._gateway, __tmp1._controlunit, Action.OFF)
        else:
            __tmp1._raspyrfm_client.send(
                __tmp1._gateway, __tmp1._controlunit, Action.ON)

        __tmp1._state = False
        __tmp1.schedule_update_ha_state()
