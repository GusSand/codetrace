"""
Support for Unifi WAP controllers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.unifi/
"""
import logging
from datetime import timedelta
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    DOMAIN, PLATFORM_SCHEMA, DeviceScanner)
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.const import CONF_VERIFY_SSL, CONF_MONITORED_CONDITIONS
import homeassistant.util.dt as dt_util

REQUIREMENTS = ['pyunifi==2.16']

_LOGGER = logging.getLogger(__name__)
CONF_PORT = 'port'
CONF_SITE_ID = 'site_id'
CONF_DETECTION_TIME = 'detection_time'
CONF_SSID_FILTER = 'ssid_filter'

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8443
DEFAULT_VERIFY_SSL = True
DEFAULT_DETECTION_TIME = timedelta(seconds=300)

NOTIFICATION_ID = 'unifi_notification'
NOTIFICATION_TITLE = 'Unifi Device Tracker Setup'

AVAILABLE_ATTRS = [
    '_id', '_is_guest_by_uap', '_last_seen_by_uap', '_uptime_by_uap',
    'ap_mac', 'assoc_time', 'authorized', 'bssid', 'bytes-r', 'ccq',
    'channel', 'essid', 'first_seen', 'hostname', 'idletime', 'ip',
    'is_11r', 'is_guest', 'is_wired', 'last_seen', 'latest_assoc_time',
    'mac', 'name', 'noise', 'noted', 'oui', 'powersave_enabled',
    'qos_policy_applied', 'radio', 'radio_proto', 'rssi', 'rx_bytes',
    'rx_bytes-r', 'rx_packets', 'rx_rate', 'signal', 'site_id',
    'tx_bytes', 'tx_bytes-r', 'tx_packets', 'tx_power', 'tx_rate',
    'uptime', 'user_id', 'usergroup_id', 'vlan'
]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Optional(CONF_SITE_ID, default='default'): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): vol.Any(
        cv.boolean, cv.isfile),
    vol.Optional(CONF_DETECTION_TIME, default=DEFAULT_DETECTION_TIME): vol.All(
        cv.time_period, cv.positive_timedelta),
    vol.Optional(CONF_MONITORED_CONDITIONS):
        vol.All(cv.ensure_list, [vol.In(AVAILABLE_ATTRS)]),
    vol.Optional(CONF_SSID_FILTER): vol.All(cv.ensure_list, [cv.string])
})


def get_scanner(hass, config):
    """Set up the Unifi device_tracker."""
    from pyunifi.controller import Controller, APIError

    host = config[DOMAIN].get(CONF_HOST)
    username = config[DOMAIN].get(CONF_USERNAME)
    password = config[DOMAIN].get(CONF_PASSWORD)
    site_id = config[DOMAIN].get(CONF_SITE_ID)
    port = config[DOMAIN].get(CONF_PORT)
    verify_ssl = config[DOMAIN].get(CONF_VERIFY_SSL)
    __tmp4 = config[DOMAIN].get(CONF_DETECTION_TIME)
    __tmp6 = config[DOMAIN].get(CONF_MONITORED_CONDITIONS)
    ssid_filter = config[DOMAIN].get(CONF_SSID_FILTER)

    try:
        ctrl = Controller(host, username, password, port, version='v4',
                          site_id=site_id, ssl_verify=verify_ssl)
    except APIError as ex:
        _LOGGER.error("Failed to connect to Unifi: %s", ex)
        hass.components.persistent_notification.create(
            'Failed to connect to Unifi. '
            'Error: {}<br />'
            'You will need to restart hass after fixing.'
            ''.format(ex),
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)
        return False

    return __typ0(ctrl, __tmp4, ssid_filter,
                        __tmp6)


class __typ0(DeviceScanner):
    """Provide device_tracker support from Unifi WAP client data."""

    def __tmp3(__tmp0, controller, __tmp4: <FILL>,
                 ssid_filter, __tmp6) :
        """Initialize the scanner."""
        __tmp0._detection_time = __tmp4
        __tmp0._controller = controller
        __tmp0._ssid_filter = ssid_filter
        __tmp0._monitored_conditions = __tmp6
        __tmp0._update()

    def _update(__tmp0):
        """Get the clients from the device."""
        from pyunifi.controller import APIError
        try:
            clients = __tmp0._controller.get_clients()
        except APIError as ex:
            _LOGGER.error("Failed to scan clients: %s", ex)
            clients = []

        # Filter clients to provided SSID list
        if __tmp0._ssid_filter:
            clients = [client for client in clients
                       if 'essid' in client and
                       client['essid'] in __tmp0._ssid_filter]

        __tmp0._clients = {
            client['mac']: client
            for client in clients
            if (dt_util.utcnow() - dt_util.utc_from_timestamp(float(
                client['last_seen']))) < __tmp0._detection_time}

    def __tmp5(__tmp0):
        """Scan for devices."""
        __tmp0._update()
        return __tmp0._clients.keys()

    def __tmp2(__tmp0, device):
        """Return the name (if known) of the device.

        If a name has been set in Unifi, then return that, else
        return the hostname if it has been detected.
        """
        client = __tmp0._clients.get(device, {})
        name = client.get('name') or client.get('hostname')
        _LOGGER.debug("Device mac %s name %s", device, name)
        return name

    def __tmp1(__tmp0, device):
        """Return the extra attributes of the device."""
        if not __tmp0._monitored_conditions:
            return {}

        client = __tmp0._clients.get(device, {})
        attributes = {}
        for variable in __tmp0._monitored_conditions:
            if variable in client:
                attributes[variable] = client[variable]

        _LOGGER.debug("Device mac %s attributes %s", device, attributes)
        return attributes
