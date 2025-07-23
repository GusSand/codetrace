"""
Reads vehicle status from BMW connected drive portal.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.bmw_connected_drive/
"""
import logging

from homeassistant.components.bmw_connected_drive import DOMAIN as BMW_DOMAIN
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.const import (CONF_UNIT_SYSTEM_IMPERIAL, VOLUME_LITERS,
                                 VOLUME_GALLONS, LENGTH_KILOMETERS,
                                 LENGTH_MILES)

DEPENDENCIES = ['bmw_connected_drive']

_LOGGER = logging.getLogger(__name__)

ATTR_TO_HA_METRIC = {
    'mileage': ['mdi:speedometer', LENGTH_KILOMETERS],
    'remaining_range_total': ['mdi:ruler', LENGTH_KILOMETERS],
    'remaining_range_electric': ['mdi:ruler', LENGTH_KILOMETERS],
    'remaining_range_fuel': ['mdi:ruler', LENGTH_KILOMETERS],
    'max_range_electric': ['mdi:ruler', LENGTH_KILOMETERS],
    'remaining_fuel': ['mdi:gas-station', VOLUME_LITERS],
    'charging_time_remaining': ['mdi:update', 'h'],
    'charging_status': ['mdi:battery-charging', None]
}

ATTR_TO_HA_IMPERIAL = {
    'mileage': ['mdi:speedometer', LENGTH_MILES],
    'remaining_range_total': ['mdi:ruler', LENGTH_MILES],
    'remaining_range_electric': ['mdi:ruler', LENGTH_MILES],
    'remaining_range_fuel': ['mdi:ruler', LENGTH_MILES],
    'max_range_electric': ['mdi:ruler', LENGTH_MILES],
    'remaining_fuel': ['mdi:gas-station', VOLUME_GALLONS],
    'charging_time_remaining': ['mdi:update', 'h'],
    'charging_status': ['mdi:battery-charging', None]
}


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the BMW sensors."""
    if hass.config.units.name == CONF_UNIT_SYSTEM_IMPERIAL:
        attribute_info = ATTR_TO_HA_IMPERIAL
    else:
        attribute_info = ATTR_TO_HA_METRIC

    accounts = hass.data[BMW_DOMAIN]
    _LOGGER.debug('Found BMW accounts: %s',
                  ', '.join([a.name for a in accounts]))
    devices = []
    for account in accounts:
        for vehicle in account.account.vehicles:
            for attribute_name in vehicle.drive_train_attributes:
                device = __typ0(account, vehicle,
                                                 attribute_name,
                                                 attribute_info)
                devices.append(device)
            device = __typ0(account, vehicle, 'mileage',
                                             attribute_info)
            devices.append(device)
    add_entities(devices, True)


class __typ0(Entity):
    """Representation of a BMW vehicle sensor."""

    def __init__(__tmp0, account, vehicle, attribute: <FILL>, attribute_info):
        """Constructor."""
        __tmp0._vehicle = vehicle
        __tmp0._account = account
        __tmp0._attribute = attribute
        __tmp0._state = None
        __tmp0._name = '{} {}'.format(__tmp0._vehicle.name, __tmp0._attribute)
        __tmp0._unique_id = '{}-{}'.format(__tmp0._vehicle.vin, __tmp0._attribute)
        __tmp0._attribute_info = attribute_info

    @property
    def should_poll(__tmp0) :
        """Return False.

        Data update is triggered from BMWConnectedDriveEntity.
        """
        return False

    @property
    def unique_id(__tmp0):
        """Return the unique ID of the sensor."""
        return __tmp0._unique_id

    @property
    def name(__tmp0) :
        """Return the name of the sensor."""
        return __tmp0._name

    @property
    def icon(__tmp0):
        """Icon to use in the frontend, if any."""
        from bimmer_connected.state import ChargingState
        vehicle_state = __tmp0._vehicle.state
        charging_state = vehicle_state.charging_status in [
            ChargingState.CHARGING]

        if __tmp0._attribute == 'charging_level_hv':
            return icon_for_battery_level(
                battery_level=vehicle_state.charging_level_hv,
                charging=charging_state)
        icon, _ = __tmp0._attribute_info.get(__tmp0._attribute, [None, None])
        return icon

    @property
    def state(__tmp0):
        """Return the state of the sensor.

        The return type of this call depends on the attribute that
        is configured.
        """
        return __tmp0._state

    @property
    def unit_of_measurement(__tmp0) :
        """Get the unit of measurement."""
        _, unit = __tmp0._attribute_info.get(__tmp0._attribute, [None, None])
        return unit

    @property
    def device_state_attributes(__tmp0):
        """Return the state attributes of the sensor."""
        return {
            'car': __tmp0._vehicle.name
        }

    def update(__tmp0) :
        """Read new state data from the library."""
        _LOGGER.debug('Updating %s', __tmp0._vehicle.name)
        vehicle_state = __tmp0._vehicle.state
        if __tmp0._attribute == 'charging_status':
            __tmp0._state = getattr(vehicle_state, __tmp0._attribute).value
        elif __tmp0.unit_of_measurement == VOLUME_GALLONS:
            value = getattr(vehicle_state, __tmp0._attribute)
            value_converted = __tmp0.hass.config.units.volume(value,
                                                            VOLUME_LITERS)
            __tmp0._state = round(value_converted)
        elif __tmp0.unit_of_measurement == LENGTH_MILES:
            value = getattr(vehicle_state, __tmp0._attribute)
            value_converted = __tmp0.hass.config.units.length(value,
                                                            LENGTH_KILOMETERS)
            __tmp0._state = round(value_converted)
        else:
            __tmp0._state = getattr(vehicle_state, __tmp0._attribute)

    def update_callback(__tmp0):
        """Schedule a state update."""
        __tmp0.schedule_update_ha_state(True)

    async def __tmp1(__tmp0):
        """Add callback after being added to hass.

        Show latest data after startup.
        """
        __tmp0._account.add_update_listener(__tmp0.update_callback)
