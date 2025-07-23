"""
Support for Tile® Bluetooth trackers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.tile/
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import (
    CONF_USERNAME, CONF_MONITORED_VARIABLES, CONF_PASSWORD)
from homeassistant.helpers.event import track_utc_time_change
from homeassistant.util import slugify
from homeassistant.util.json import load_json, save_json

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pytile==1.0.0']

CLIENT_UUID_CONFIG_FILE = '.tile.conf'
DEFAULT_ICON = 'mdi:bluetooth'
DEVICE_TYPES = ['PHONE', 'TILE']

ATTR_ALTITUDE = 'altitude'
ATTR_CONNECTION_STATE = 'connection_state'
ATTR_IS_DEAD = 'is_dead'
ATTR_IS_LOST = 'is_lost'
ATTR_LAST_SEEN = 'last_seen'
ATTR_LAST_UPDATED = 'last_updated'
ATTR_RING_STATE = 'ring_state'
ATTR_VOIP_STATE = 'voip_state'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_MONITORED_VARIABLES):
        vol.All(cv.ensure_list, [vol.In(DEVICE_TYPES)]),
})


def __tmp3(__tmp0, config: <FILL>, see, discovery_info=None):
    """Validate the configuration and return a Tile scanner."""
    TileDeviceScanner(__tmp0, config, see)
    return True


class TileDeviceScanner(DeviceScanner):
    """Define a device scanner for Tiles."""

    def __tmp2(__tmp1, __tmp0, config, see):
        """Initialize."""
        from pytile import Client

        _LOGGER.debug('Received configuration data: %s', config)

        # Load the client UUID (if it exists):
        config_data = load_json(__tmp0.config.path(CLIENT_UUID_CONFIG_FILE))
        if config_data:
            _LOGGER.debug('Using existing client UUID')
            __tmp1._client = Client(
                config[CONF_USERNAME],
                config[CONF_PASSWORD],
                config_data['client_uuid'])
        else:
            _LOGGER.debug('Generating new client UUID')
            __tmp1._client = Client(
                config[CONF_USERNAME],
                config[CONF_PASSWORD])

            if not save_json(
                    __tmp0.config.path(CLIENT_UUID_CONFIG_FILE),
                    {'client_uuid': __tmp1._client.client_uuid}):
                _LOGGER.error("Failed to save configuration file")

        _LOGGER.debug('Client UUID: %s', __tmp1._client.client_uuid)
        _LOGGER.debug('User UUID: %s', __tmp1._client.user_uuid)

        __tmp1._types = config.get(CONF_MONITORED_VARIABLES)

        __tmp1.devices = {}
        __tmp1.see = see

        track_utc_time_change(
            __tmp0, __tmp1._update_info, second=range(0, 60, 30))

        __tmp1._update_info()

    def _update_info(__tmp1, now=None) -> None:
        """Update the device info."""
        device_data = __tmp1._client.get_tiles(type_whitelist=__tmp1._types)

        try:
            __tmp1.devices = device_data['result']
        except KeyError:
            _LOGGER.warning('No Tiles found')
            _LOGGER.debug(device_data)
            return

        for info in __tmp1.devices.values():
            dev_id = 'tile_{0}'.format(slugify(info['name']))
            lat = info['tileState']['latitude']
            lon = info['tileState']['longitude']

            attrs = {
                ATTR_ALTITUDE: info['tileState']['altitude'],
                ATTR_CONNECTION_STATE: info['tileState']['connection_state'],
                ATTR_IS_DEAD: info['is_dead'],
                ATTR_IS_LOST: info['tileState']['is_lost'],
                ATTR_LAST_SEEN: info['tileState']['timestamp'],
                ATTR_LAST_UPDATED: device_data['timestamp_ms'],
                ATTR_RING_STATE: info['tileState']['ring_state'],
                ATTR_VOIP_STATE: info['tileState']['voip_state'],
            }

            __tmp1.see(
                dev_id=dev_id,
                gps=(lat, lon),
                attributes=attrs,
                icon=DEFAULT_ICON
            )
