from typing import TypeAlias
__typ0 : TypeAlias = "dict"
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


def setup(__tmp3, config: __typ0):
    """Set up the BMW connected drive components."""
    accounts = []
    for name, account_config in config[DOMAIN].items():
        accounts.append(__tmp9(account_config, __tmp3, name))

    __tmp3.data[DOMAIN] = accounts

    def __tmp5(__tmp6) :
        """Update all BMW accounts."""
        for cd_account in __tmp3.data[DOMAIN]:
            cd_account.update()

    # Service to manually trigger updates for all accounts.
    __tmp3.services.register(DOMAIN, SERVICE_UPDATE_STATE, __tmp5)

    __tmp5(None)

    for component in BMW_COMPONENTS:
        discovery.load_platform(__tmp3, component, DOMAIN, {}, config)

    return True


def __tmp9(account_config, __tmp3, name: <FILL>) \
        :
    """Set up a new BMWConnectedDriveAccount based on the config."""
    __tmp2 = account_config[CONF_USERNAME]
    __tmp4 = account_config[CONF_PASSWORD]
    region = account_config[CONF_REGION]
    read_only = account_config[CONF_READ_ONLY]

    _LOGGER.debug('Adding new account %s', name)
    cd_account = BMWConnectedDriveAccount(__tmp2, __tmp4, region, name,
                                          read_only)

    def __tmp8(__tmp6):
        """Execute a service for a vehicle.

        This must be a member function as we need access to the cd_account
        object here.
        """
        vin = __tmp6.data[ATTR_VIN]
        vehicle = cd_account.account.get_vehicle(vin)
        if not vehicle:
            _LOGGER.error('Could not find a vehicle for VIN "%s"!', vin)
            return
        function_name = _SERVICE_MAP[__tmp6.service]
        function_call = getattr(vehicle.remote_services, function_name)
        function_call()
    if not read_only:
        # register the remote services
        for service in _SERVICE_MAP:
            __tmp3.services.register(
                DOMAIN, service,
                __tmp8,
                schema=SERVICE_SCHEMA)

    # update every UPDATE_INTERVAL minutes, starting now
    # this should even out the load on the servers
    now = datetime.datetime.now()
    track_utc_time_change(
        __tmp3, cd_account.update,
        minute=range(now.minute % UPDATE_INTERVAL, 60, UPDATE_INTERVAL),
        second=now.second)

    return cd_account


class BMWConnectedDriveAccount:
    """Representation of a BMW vehicle."""

    def __tmp7(__tmp0, __tmp2, __tmp4, __tmp1,
                 name, read_only) :
        """Constructor."""
        from bimmer_connected.account import ConnectedDriveAccount
        from bimmer_connected.country_selector import get_region_from_name

        region = get_region_from_name(__tmp1)

        __tmp0.read_only = read_only
        __tmp0.account = ConnectedDriveAccount(__tmp2, __tmp4, region)
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
            for listener in __tmp0._update_listeners:
                listener()
        except IOError as exception:
            _LOGGER.error('Error updating the vehicle state.')
            _LOGGER.exception(exception)

    def add_update_listener(__tmp0, listener):
        """Add a listener for update notifications."""
        __tmp0._update_listeners.append(listener)
