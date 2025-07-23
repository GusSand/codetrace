from typing import TypeAlias
__typ1 : TypeAlias = "dict"
"""
Reads vehicle status from BMW connected drive portal.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/bmw_connected_drive/
"""
import datetime
import logging

import voluptuous as vol

from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD)
from homeassistant.helpers import discovery
from homeassistant.helpers.event import track_utc_time_change
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['bimmer_connected==0.5.3']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'bmw_connected_drive'
CONF_REGION = 'region'
CONF_READ_ONLY = 'read_only'
ATTR_VIN = 'vin'

ACCOUNT_SCHEMA = vol.Schema({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_REGION): vol.Any('north_america', 'china',
                                       'rest_of_world'),
    vol.Optional(CONF_READ_ONLY, default=False): cv.boolean,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: {
        cv.string: ACCOUNT_SCHEMA
    },
}, extra=vol.ALLOW_EXTRA)

SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_VIN): cv.string,
})


BMW_COMPONENTS = ['binary_sensor', 'device_tracker', 'lock', 'sensor']
UPDATE_INTERVAL = 5  # in minutes

SERVICE_UPDATE_STATE = 'update_state'

_SERVICE_MAP = {
    'light_flash': 'trigger_remote_light_flash',
    'sound_horn': 'trigger_remote_horn',
    'activate_air_conditioning': 'trigger_remote_air_conditioning',
}


def setup(__tmp5, config: __typ1):
    """Set up the BMW connected drive components."""
    accounts = []
    for name, account_config in config[DOMAIN].items():
        accounts.append(setup_account(account_config, __tmp5, name))

    __tmp5.data[DOMAIN] = accounts

    def __tmp3(call) :
        """Update all BMW accounts."""
        for cd_account in __tmp5.data[DOMAIN]:
            cd_account.update()

    # Service to manually trigger updates for all accounts.
    __tmp5.services.register(DOMAIN, SERVICE_UPDATE_STATE, __tmp3)

    __tmp3(None)

    for component in BMW_COMPONENTS:
        discovery.load_platform(__tmp5, component, DOMAIN, {}, config)

    return True


def setup_account(account_config: __typ1, __tmp5, name: str) \
        :
    """Set up a new BMWConnectedDriveAccount based on the config."""
    username = account_config[CONF_USERNAME]
    password = account_config[CONF_PASSWORD]
    region = account_config[CONF_REGION]
    read_only = account_config[CONF_READ_ONLY]

    _LOGGER.debug('Adding new account %s', name)
    cd_account = __typ0(username, password, region, name,
                                          read_only)

    def __tmp4(call):
        """Execute a service for a vehicle.

        This must be a member function as we need access to the cd_account
        object here.
        """
        vin = call.data[ATTR_VIN]
        vehicle = cd_account.account.get_vehicle(vin)
        if not vehicle:
            _LOGGER.error('Could not find a vehicle for VIN "%s"!', vin)
            return
        function_name = _SERVICE_MAP[call.service]
        function_call = getattr(vehicle.remote_services, function_name)
        function_call()
    if not read_only:
        # register the remote services
        for service in _SERVICE_MAP:
            __tmp5.services.register(
                DOMAIN, service,
                __tmp4,
                schema=SERVICE_SCHEMA)

    # update every UPDATE_INTERVAL minutes, starting now
    # this should even out the load on the servers
    now = datetime.datetime.now()
    track_utc_time_change(
        __tmp5, cd_account.update,
        minute=range(now.minute % UPDATE_INTERVAL, 60, UPDATE_INTERVAL),
        second=now.second)

    return cd_account


class __typ0:
    """Representation of a BMW vehicle."""

    def __init__(__tmp0, username: <FILL>, password, region_str,
                 name: str, read_only) -> None:
        """Constructor."""
        from bimmer_connected.account import ConnectedDriveAccount
        from bimmer_connected.country_selector import get_region_from_name

        region = get_region_from_name(region_str)

        __tmp0.read_only = read_only
        __tmp0.account = ConnectedDriveAccount(username, password, region)
        __tmp0.name = name
        __tmp0._update_listeners = []

    def update(__tmp0, *_):
        """Update the state of all vehicles.

        Notify all listeners about the update.
        """
        _LOGGER.debug('Updating vehicle state for account %s, '
                      'notifying %d listeners',
                      __tmp0.name, len(__tmp0._update_listeners))
        try:
            __tmp0.account.update_vehicle_states()
            for __tmp1 in __tmp0._update_listeners:
                __tmp1()
        except IOError as exception:
            _LOGGER.error('Error updating the vehicle state.')
            _LOGGER.exception(exception)

    def __tmp2(__tmp0, __tmp1):
        """Add a listener for update notifications."""
        __tmp0._update_listeners.append(__tmp1)
