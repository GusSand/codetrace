"""Parent component for Ecovacs Deebot vacuums.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/ecovacs/
"""

import logging
import random
import string

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, \
    EVENT_HOMEASSISTANT_STOP

REQUIREMENTS = ['sucks==0.9.3']

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ecovacs"

CONF_COUNTRY = "country"
CONF_CONTINENT = "continent"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(CONF_COUNTRY): vol.All(vol.Lower, cv.string),
        vol.Required(CONF_CONTINENT): vol.All(vol.Lower, cv.string),
    })
}, extra=vol.ALLOW_EXTRA)

ECOVACS_DEVICES = "ecovacs_devices"

# Generate a random device ID on each bootup
ECOVACS_API_DEVICEID = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for _ in range(8)
)


def __tmp1(__tmp2, config):
    """Set up the Ecovacs component."""
    _LOGGER.debug("Creating new Ecovacs component")

    __tmp2.data[ECOVACS_DEVICES] = []

    from sucks import EcoVacsAPI, VacBot

    ecovacs_api = EcoVacsAPI(ECOVACS_API_DEVICEID,
                             config[DOMAIN].get(CONF_USERNAME),
                             EcoVacsAPI.md5(config[DOMAIN].get(CONF_PASSWORD)),
                             config[DOMAIN].get(CONF_COUNTRY),
                             config[DOMAIN].get(CONF_CONTINENT))

    devices = ecovacs_api.devices()
    _LOGGER.debug("Ecobot devices: %s", devices)

    for device in devices:
        _LOGGER.info(
            "Discovered Ecovacs device on account: %s with nickname %s",
            device['did'], device['nick'])
        vacbot = VacBot(ecovacs_api.uid,
                        ecovacs_api.REALM,
                        ecovacs_api.resource,
                        ecovacs_api.user_access_token,
                        device,
                        config[DOMAIN].get(CONF_CONTINENT).lower(),
                        monitor=True)
        __tmp2.data[ECOVACS_DEVICES].append(vacbot)

    def __tmp0(__tmp3: <FILL>) -> None:
        """Shut down open connections to Ecovacs XMPP server."""
        for device in __tmp2.data[ECOVACS_DEVICES]:
            _LOGGER.info("Shutting down connection to Ecovacs device %s",
                         device.vacuum['did'])
            device.disconnect()

    # Listen for HA stop to disconnect.
    __tmp2.bus.listen_once(EVENT_HOMEASSISTANT_STOP, __tmp0)

    if __tmp2.data[ECOVACS_DEVICES]:
        _LOGGER.debug("Starting vacuum components")
        discovery.load_platform(__tmp2, "vacuum", DOMAIN, {}, config)

    return True
