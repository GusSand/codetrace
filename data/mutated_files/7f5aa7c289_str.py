from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""
Sensor platform to display the current fuel prices at a NSW fuel station.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.nsw_fuel_station/
"""
import datetime
import logging
from typing import Optional

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.light import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

REQUIREMENTS = ['nsw-fuel-api-client==1.0.10']

_LOGGER = logging.getLogger(__name__)

ATTR_STATION_ID = 'station_id'
ATTR_STATION_NAME = 'station_name'

CONF_STATION_ID = 'station_id'
CONF_FUEL_TYPES = 'fuel_types'
CONF_ALLOWED_FUEL_TYPES = ["E10", "U91", "E85", "P95", "P98", "DL",
                           "PDL", "B20", "LPG", "CNG", "EV"]
CONF_DEFAULT_FUEL_TYPES = ["E10", "U91"]
CONF_ATTRIBUTION = "Data provided by NSW Government FuelCheck"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_STATION_ID): cv.positive_int,
    vol.Optional(CONF_FUEL_TYPES, default=CONF_DEFAULT_FUEL_TYPES):
        vol.All(cv.ensure_list, [vol.In(CONF_ALLOWED_FUEL_TYPES)]),
})

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(hours=1)

NOTIFICATION_ID = 'nsw_fuel_station_notification'
NOTIFICATION_TITLE = 'NSW Fuel Station Sensor Setup'


def __tmp2(hass, config, __tmp1, discovery_info=None):
    """Set up the NSW Fuel Station sensor."""
    from nsw_fuel import FuelCheckClient

    station_id = config[CONF_STATION_ID]
    fuel_types = config[CONF_FUEL_TYPES]

    __tmp5 = FuelCheckClient()
    __tmp3 = StationPriceData(__tmp5, station_id)
    __tmp3.update()

    if __tmp3.error is not None:
        message = (
            'Error: {}. Check the logs for additional information.'
        ).format(__tmp3.error)

        hass.components.persistent_notification.create(
            message,
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)
        return

    available_fuel_types = __tmp3.get_available_fuel_types()

    __tmp1([
        StationPriceSensor(__tmp3, fuel_type)
        for fuel_type in fuel_types
        if fuel_type in available_fuel_types
    ])


class StationPriceData:
    """An object to store and fetch the latest data for a given station."""

    def __init__(__tmp0, __tmp5, station_id) :
        """Initialize the sensor."""
        __tmp0.station_id = station_id
        __tmp0._client = __tmp5
        __tmp0._data = None
        __tmp0._reference_data = None
        __tmp0.error = None
        __tmp0._station_name = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(__tmp0):
        """Update the internal data using the API client."""
        from nsw_fuel import FuelCheckError

        if __tmp0._reference_data is None:
            try:
                __tmp0._reference_data = __tmp0._client.get_reference_data()
            except FuelCheckError as exc:
                __tmp0.error = str(exc)
                _LOGGER.error(
                    'Failed to fetch NSW Fuel station reference data. %s', exc)
                return

        try:
            __tmp0._data = __tmp0._client.get_fuel_prices_for_station(
                __tmp0.station_id)
        except FuelCheckError as exc:
            __tmp0.error = str(exc)
            _LOGGER.error(
                'Failed to fetch NSW Fuel station price data. %s', exc)

    def for_fuel_type(__tmp0, fuel_type: <FILL>):
        """Return the price of the given fuel type."""
        if __tmp0._data is None:
            return None
        return next((price for price
                     in __tmp0._data if price.fuel_type == fuel_type), None)

    def get_available_fuel_types(__tmp0):
        """Return the available fuel types for the station."""
        return [price.fuel_type for price in __tmp0._data]

    def get_station_name(__tmp0) :
        """Return the name of the station."""
        if __tmp0._station_name is None:
            name = None
            if __tmp0._reference_data is not None:
                name = next((station.name for station
                             in __tmp0._reference_data.stations
                             if station.code == __tmp0.station_id), None)

            __tmp0._station_name = name or 'station {}'.format(__tmp0.station_id)

        return __tmp0._station_name


class StationPriceSensor(Entity):
    """Implementation of a sensor that reports the fuel price for a station."""

    def __init__(__tmp0, __tmp3, fuel_type):
        """Initialize the sensor."""
        __tmp0._station_data = __tmp3
        __tmp0._fuel_type = fuel_type

    @property
    def name(__tmp0) :
        """Return the name of the sensor."""
        return '{} {}'.format(
            __tmp0._station_data.get_station_name(), __tmp0._fuel_type)

    @property
    def state(__tmp0) :
        """Return the state of the sensor."""
        price_info = __tmp0._station_data.for_fuel_type(__tmp0._fuel_type)
        if price_info:
            return price_info.price

        return None

    @property
    def device_state_attributes(__tmp0) :
        """Return the state attributes of the device."""
        return {
            ATTR_STATION_ID: __tmp0._station_data.station_id,
            ATTR_STATION_NAME: __tmp0._station_data.get_station_name(),
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION
        }

    @property
    def __tmp4(__tmp0) :
        """Return the units of measurement."""
        return '¢/L'

    def update(__tmp0):
        """Update current conditions."""
        __tmp0._station_data.update()
