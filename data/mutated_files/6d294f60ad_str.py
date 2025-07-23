"""
Support for Geofency.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/geofency/
"""
import logging

import voluptuous as vol
from aiohttp import web

import homeassistant.helpers.config_validation as cv
from homeassistant.const import HTTP_UNPROCESSABLE_ENTITY, STATE_NOT_HOME, \
    ATTR_LATITUDE, ATTR_LONGITUDE, CONF_WEBHOOK_ID, HTTP_OK, ATTR_NAME
from homeassistant.helpers import config_entry_flow
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'geofency'
DEPENDENCIES = ['webhook']

CONF_MOBILE_BEACONS = 'mobile_beacons'

CONFIG_SCHEMA = vol.Schema({
    vol.Optional(DOMAIN): vol.Schema({
        vol.Optional(CONF_MOBILE_BEACONS, default=[]): vol.All(
            cv.ensure_list,
            [cv.string]
        ),
    }),
}, extra=vol.ALLOW_EXTRA)

ATTR_ADDRESS = 'address'
ATTR_BEACON_ID = 'beaconUUID'
ATTR_CURRENT_LATITUDE = 'currentLatitude'
ATTR_CURRENT_LONGITUDE = 'currentLongitude'
ATTR_DEVICE = 'device'
ATTR_ENTRY = 'entry'

BEACON_DEV_PREFIX = 'beacon'

LOCATION_ENTRY = '1'
LOCATION_EXIT = '0'

TRACKER_UPDATE = '{}_tracker_update'.format(DOMAIN)


def __tmp4(value: <FILL>) :
    r"""Coerce address by replacing '\n' with ' '."""
    return value.replace('\n', ' ')


WEBHOOK_SCHEMA = vol.Schema({
    vol.Required(ATTR_ADDRESS): vol.All(cv.string, __tmp4),
    vol.Required(ATTR_DEVICE): vol.All(cv.string, slugify),
    vol.Required(ATTR_ENTRY): vol.Any(LOCATION_ENTRY, LOCATION_EXIT),
    vol.Required(ATTR_LATITUDE): cv.latitude,
    vol.Required(ATTR_LONGITUDE): cv.longitude,
    vol.Required(ATTR_NAME): vol.All(cv.string, slugify),
    vol.Optional(ATTR_CURRENT_LATITUDE): cv.latitude,
    vol.Optional(ATTR_CURRENT_LONGITUDE): cv.longitude,
    vol.Optional(ATTR_BEACON_ID): cv.string
}, extra=vol.ALLOW_EXTRA)


async def async_setup(__tmp7, __tmp2):
    """Set up the Geofency component."""
    config = __tmp2[DOMAIN]
    mobile_beacons = config[CONF_MOBILE_BEACONS]
    __tmp7.data[DOMAIN] = [slugify(beacon) for beacon in mobile_beacons]

    __tmp7.async_create_task(
        async_load_platform(__tmp7, 'device_tracker', DOMAIN, {}, __tmp2)
    )
    return True


async def handle_webhook(__tmp7, __tmp1, __tmp6):
    """Handle incoming webhook from Geofency."""
    try:
        data = WEBHOOK_SCHEMA(dict(await __tmp6.post()))
    except vol.MultipleInvalid as error:
        return web.Response(
            body=error.error_message,
            status=HTTP_UNPROCESSABLE_ENTITY
        )

    if __tmp3(data, __tmp7.data[DOMAIN]):
        return __tmp8(__tmp7, data, None)
    if data['entry'] == LOCATION_ENTRY:
        __tmp5 = data['name']
    else:
        __tmp5 = STATE_NOT_HOME
        if ATTR_CURRENT_LATITUDE in data:
            data[ATTR_LATITUDE] = data[ATTR_CURRENT_LATITUDE]
            data[ATTR_LONGITUDE] = data[ATTR_CURRENT_LONGITUDE]

    return __tmp8(__tmp7, data, __tmp5)


def __tmp3(data, mobile_beacons):
    """Check if we have a mobile beacon."""
    return ATTR_BEACON_ID in data and data['name'] in mobile_beacons


def _device_name(data):
    """Return name of device tracker."""
    if ATTR_BEACON_ID in data:
        return "{}_{}".format(BEACON_DEV_PREFIX, data['name'])
    return data['device']


def __tmp8(__tmp7, data, __tmp5):
    """Fire HA event to set location."""
    device = _device_name(data)

    async_dispatcher_send(
        __tmp7,
        TRACKER_UPDATE,
        device,
        (data[ATTR_LATITUDE], data[ATTR_LONGITUDE]),
        __tmp5,
        data
    )

    return web.Response(
        body="Setting location for {}".format(device),
        status=HTTP_OK
    )


async def __tmp0(__tmp7, entry):
    """Configure based on config entry."""
    __tmp7.components.webhook.async_register(
        DOMAIN, 'Geofency', entry.data[CONF_WEBHOOK_ID], handle_webhook)
    return True


async def async_unload_entry(__tmp7, entry):
    """Unload a config entry."""
    __tmp7.components.webhook.async_unregister(entry.data[CONF_WEBHOOK_ID])
    return True

config_entry_flow.register_webhook_flow(
    DOMAIN,
    'Geofency Webhook',
    {
        'docs_url': 'https://www.home-assistant.io/components/geofency/'
    }
)
