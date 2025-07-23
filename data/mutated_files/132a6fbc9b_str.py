from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "dict"
"""
Real-time information about public transport departures in Norway.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.entur_public_transport/
"""
from datetime import datetime, timedelta
import logging

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_ATTRIBUTION, CONF_LATITUDE, CONF_LONGITUDE, CONF_NAME,
    CONF_SHOW_ON_MAP)
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util

REQUIREMENTS = ['enturclient==0.1.3']

_LOGGER = logging.getLogger(__name__)

ATTR_NEXT_UP_IN = 'next_due_in'

API_CLIENT_NAME = 'homeassistant-homeassistant'

CONF_ATTRIBUTION = "Data provided by entur.org under NLOD."
CONF_STOP_IDS = 'stop_ids'
CONF_EXPAND_PLATFORMS = 'expand_platforms'
CONF_WHITELIST_LINES = 'line_whitelist'

DEFAULT_NAME = 'Entur'
DEFAULT_ICON_KEY = 'bus'

ICONS = {
    'air': 'mdi:airplane',
    'bus': 'mdi:bus',
    'metro': 'mdi:subway',
    'rail': 'mdi:train',
    'tram': 'mdi:tram',
    'water': 'mdi:ferry',
}

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STOP_IDS): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_EXPAND_PLATFORMS, default=True): cv.boolean,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SHOW_ON_MAP, default=False): cv.boolean,
    vol.Optional(CONF_WHITELIST_LINES, default=[]): cv.ensure_list,
})


def __tmp11(__tmp7: str) -> str:
    """Get the time in minutes from a timestamp.

    The timestamp should be in the format
    year-month-yearThour:minute:second+timezone
    """
    if __tmp7 is None:
        return None
    diff = datetime.strptime(
        __tmp7, "%Y-%m-%dT%H:%M:%S%z") - dt_util.now()

    return str(int(diff.total_seconds() / 60))


def __tmp3(__tmp12, config, __tmp1, discovery_info=None):
    """Set up the Entur public transport sensor."""
    from enturclient import EnturPublicTransportData
    from enturclient.consts import CONF_NAME as API_NAME

    expand = config.get(CONF_EXPAND_PLATFORMS)
    line_whitelist = config.get(CONF_WHITELIST_LINES)
    __tmp14 = config.get(CONF_NAME)
    __tmp9 = config.get(CONF_SHOW_ON_MAP)
    stop_ids = config.get(CONF_STOP_IDS)

    stops = [s for s in stop_ids if "StopPlace" in s]
    quays = [s for s in stop_ids if "Quay" in s]

    data = EnturPublicTransportData(API_CLIENT_NAME,
                                    stops,
                                    quays,
                                    expand,
                                    line_whitelist)
    data.update()

    proxy = __typ1(data)

    entities = []
    for item in data.all_stop_places_quays():
        try:
            given_name = "{} {}".format(
                __tmp14, data.get_stop_info(item)[API_NAME])
        except KeyError:
            given_name = "{} {}".format(__tmp14, item)

        entities.append(
            __typ0(proxy, given_name, item, __tmp9))

    __tmp1(entities, True)


class __typ1:
    """Proxy for the Entur client.

    Ensure throttle to not hit rate limiting on the API.
    """

    def __tmp8(__tmp0, api):
        """Initialize the proxy."""
        __tmp0._api = api

    @Throttle(SCAN_INTERVAL)
    def update(__tmp0) -> None:
        """Update data in client."""
        __tmp0._api.update()

    def get_stop_info(__tmp0, __tmp13) -> __typ3:
        """Get info about specific stop place."""
        return __tmp0._api.get_stop_info(__tmp13)


class __typ0(Entity):
    """Implementation of a Entur public transport sensor."""

    def __tmp8(
            __tmp0, api: __typ1, __tmp14: <FILL>, __tmp5: str, __tmp9: __typ2):
        """Initialize the sensor."""
        from enturclient.consts import ATTR_STOP_ID

        __tmp0.api = api
        __tmp0._stop = __tmp5
        __tmp0._show_on_map = __tmp9
        __tmp0._name = __tmp14
        __tmp0._state = None
        __tmp0._icon = ICONS[DEFAULT_ICON_KEY]
        __tmp0._attributes = {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
            ATTR_STOP_ID: __tmp0._stop,
        }

    @property
    def __tmp14(__tmp0) -> str:
        """Return the name of the sensor."""
        return __tmp0._name

    @property
    def __tmp4(__tmp0) -> str:
        """Return the state of the sensor."""
        return __tmp0._state

    @property
    def __tmp2(__tmp0) -> __typ3:
        """Return the state attributes."""
        return __tmp0._attributes

    @property
    def __tmp6(__tmp0) -> str:
        """Return the unit this state is expressed in."""
        return 'min'

    @property
    def __tmp10(__tmp0) -> str:
        """Icon to use in the frontend."""
        return __tmp0._icon

    def update(__tmp0) -> None:
        """Get the latest data and update the states."""
        from enturclient.consts import (
            ATTR, ATTR_EXPECTED_AT, ATTR_NEXT_UP_AT, CONF_LOCATION,
            CONF_LATITUDE as LAT, CONF_LONGITUDE as LONG, CONF_TRANSPORT_MODE)

        __tmp0.api.update()

        data = __tmp0.api.get_stop_info(__tmp0._stop)
        if data is not None and ATTR in data:
            attrs = data[ATTR]
            __tmp0._attributes.update(attrs)

            if ATTR_NEXT_UP_AT in attrs:
                __tmp0._attributes[ATTR_NEXT_UP_IN] = \
                    __tmp11(attrs[ATTR_NEXT_UP_AT])

            if CONF_LOCATION in data and __tmp0._show_on_map:
                __tmp0._attributes[CONF_LATITUDE] = data[CONF_LOCATION][LAT]
                __tmp0._attributes[CONF_LONGITUDE] = data[CONF_LOCATION][LONG]

            if ATTR_EXPECTED_AT in attrs:
                __tmp0._state = __tmp11(attrs[ATTR_EXPECTED_AT])
            else:
                __tmp0._state = None

            __tmp0._icon = ICONS.get(
                data[CONF_TRANSPORT_MODE], ICONS[DEFAULT_ICON_KEY])
        else:
            __tmp0._state = None
