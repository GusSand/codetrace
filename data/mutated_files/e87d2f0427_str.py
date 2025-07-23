"""
Support for BMW cars with BMW ConnectedDrive.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/lock.bmw_connected_drive/
"""
import logging

from homeassistant.components.bmw_connected_drive import DOMAIN as BMW_DOMAIN
from homeassistant.components.lock import LockDevice
from homeassistant.const import STATE_LOCKED, STATE_UNLOCKED

DEPENDENCIES = ['bmw_connected_drive']

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the BMW Connected Drive lock."""
    accounts = hass.data[BMW_DOMAIN]
    _LOGGER.debug('Found BMW accounts: %s',
                  ', '.join([a.name for a in accounts]))
    devices = []
    for account in accounts:
        if not account.read_only:
            for vehicle in account.account.vehicles:
                device = __typ0(account, vehicle, 'lock', 'BMW lock')
                devices.append(device)
    add_entities(devices, True)


class __typ0(LockDevice):
    """Representation of a BMW vehicle lock."""

    def __tmp3(__tmp0, account, vehicle, __tmp2: <FILL>, sensor_name):
        """Initialize the lock."""
        __tmp0._account = account
        __tmp0._vehicle = vehicle
        __tmp0._attribute = __tmp2
        __tmp0._name = '{} {}'.format(__tmp0._vehicle.name, __tmp0._attribute)
        __tmp0._unique_id = '{}-{}'.format(__tmp0._vehicle.vin, __tmp0._attribute)
        __tmp0._sensor_name = sensor_name
        __tmp0._state = None

    @property
    def __tmp4(__tmp0):
        """Do not poll this class.

        Updates are triggered from BMWConnectedDriveAccount.
        """
        return False

    @property
    def unique_id(__tmp0):
        """Return the unique ID of the lock."""
        return __tmp0._unique_id

    @property
    def name(__tmp0):
        """Return the name of the lock."""
        return __tmp0._name

    @property
    def device_state_attributes(__tmp0):
        """Return the state attributes of the lock."""
        vehicle_state = __tmp0._vehicle.state
        return {
            'car': __tmp0._vehicle.name,
            'door_lock_state': vehicle_state.door_lock_state.value
        }

    @property
    def __tmp1(__tmp0):
        """Return true if lock is locked."""
        return __tmp0._state == STATE_LOCKED

    def lock(__tmp0, **kwargs):
        """Lock the car."""
        _LOGGER.debug("%s: locking doors", __tmp0._vehicle.name)
        # Optimistic state set here because it takes some time before the
        # update callback response
        __tmp0._state = STATE_LOCKED
        __tmp0.schedule_update_ha_state()
        __tmp0._vehicle.remote_services.trigger_remote_door_lock()

    def unlock(__tmp0, **kwargs):
        """Unlock the car."""
        _LOGGER.debug("%s: unlocking doors", __tmp0._vehicle.name)
        # Optimistic state set here because it takes some time before the
        # update callback response
        __tmp0._state = STATE_UNLOCKED
        __tmp0.schedule_update_ha_state()
        __tmp0._vehicle.remote_services.trigger_remote_door_unlock()

    def update(__tmp0):
        """Update state of the lock."""
        from bimmer_connected.state import LockState

        _LOGGER.debug("%s: updating data for %s", __tmp0._vehicle.name,
                      __tmp0._attribute)
        vehicle_state = __tmp0._vehicle.state

        # Possible values: LOCKED, SECURED, SELECTIVE_LOCKED, UNLOCKED
        __tmp0._state = STATE_LOCKED \
            if vehicle_state.door_lock_state \
            in [LockState.LOCKED, LockState.SECURED] \
            else STATE_UNLOCKED

    def update_callback(__tmp0):
        """Schedule a state update."""
        __tmp0.schedule_update_ha_state(True)

    async def async_added_to_hass(__tmp0):
        """Add callback after being added to hass.

        Show latest data after startup.
        """
        __tmp0._account.add_update_listener(__tmp0.update_callback)
