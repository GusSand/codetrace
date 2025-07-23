from typing import TypeAlias
__typ1 : TypeAlias = "ComfoConnectBridge"
__typ2 : TypeAlias = "int"
"""
Platform to control a Zehnder ComfoAir Q350/450/600 ventilation unit.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/fan.comfoconnect/
"""
import logging

from homeassistant.components.comfoconnect import (
    DOMAIN, ComfoConnectBridge, SIGNAL_COMFOCONNECT_UPDATE_RECEIVED)
from homeassistant.components.fan import (
    FanEntity, SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH,
    SUPPORT_SET_SPEED)
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.dispatcher import (dispatcher_connect)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['comfoconnect']

SPEED_MAPPING = {
    0: SPEED_OFF,
    1: SPEED_LOW,
    2: SPEED_MEDIUM,
    3: SPEED_HIGH
}


def __tmp1(__tmp10, config, add_entities, discovery_info=None):
    """Set up the ComfoConnect fan platform."""
    __tmp2 = __tmp10.data[DOMAIN]

    add_entities([__typ0(__tmp10, name=__tmp2.name, __tmp2=__tmp2)], True)


class __typ0(FanEntity):
    """Representation of the ComfoConnect fan platform."""

    def __tmp9(__tmp0, __tmp10, name, __tmp2) :
        """Initialize the ComfoConnect fan."""
        from pycomfoconnect import SENSOR_FAN_SPEED_MODE

        __tmp0._ccb = __tmp2
        __tmp0._name = name

        # Ask the bridge to keep us updated
        __tmp0._ccb.comfoconnect.register_sensor(SENSOR_FAN_SPEED_MODE)

        def __tmp11(__tmp5):
            if __tmp5 == SENSOR_FAN_SPEED_MODE:
                _LOGGER.debug("Dispatcher update for %s", __tmp5)
                __tmp0.schedule_update_ha_state()

        # Register for dispatcher updates
        dispatcher_connect(
            __tmp10, SIGNAL_COMFOCONNECT_UPDATE_RECEIVED, __tmp11)

    @property
    def name(__tmp0):
        """Return the name of the fan."""
        return __tmp0._name

    @property
    def __tmp4(__tmp0):
        """Return the icon to use in the frontend."""
        return 'mdi:air-conditioner'

    @property
    def __tmp12(__tmp0) :
        """Flag supported features."""
        return SUPPORT_SET_SPEED

    @property
    def __tmp6(__tmp0):
        """Return the current fan mode."""
        from pycomfoconnect import (SENSOR_FAN_SPEED_MODE)

        try:
            __tmp6 = __tmp0._ccb.data[SENSOR_FAN_SPEED_MODE]
            return SPEED_MAPPING[__tmp6]
        except KeyError:
            return STATE_UNKNOWN

    @property
    def __tmp7(__tmp0):
        """List of available fan modes."""
        return [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    def __tmp8(__tmp0, __tmp6: str = None, **kwargs) -> None:
        """Turn on the fan."""
        if __tmp6 is None:
            __tmp6 = SPEED_LOW
        __tmp0.set_speed(__tmp6)

    def __tmp3(__tmp0, **kwargs) :
        """Turn off the fan (to away)."""
        __tmp0.set_speed(SPEED_OFF)

    def set_speed(__tmp0, __tmp6: <FILL>):
        """Set fan speed."""
        _LOGGER.debug('Changing fan speed to %s.', __tmp6)

        from pycomfoconnect import (
            CMD_FAN_MODE_AWAY, CMD_FAN_MODE_LOW, CMD_FAN_MODE_MEDIUM,
            CMD_FAN_MODE_HIGH)

        if __tmp6 == SPEED_OFF:
            __tmp0._ccb.comfoconnect.cmd_rmi_request(CMD_FAN_MODE_AWAY)
        elif __tmp6 == SPEED_LOW:
            __tmp0._ccb.comfoconnect.cmd_rmi_request(CMD_FAN_MODE_LOW)
        elif __tmp6 == SPEED_MEDIUM:
            __tmp0._ccb.comfoconnect.cmd_rmi_request(CMD_FAN_MODE_MEDIUM)
        elif __tmp6 == SPEED_HIGH:
            __tmp0._ccb.comfoconnect.cmd_rmi_request(CMD_FAN_MODE_HIGH)

        # Update current mode
        __tmp0.schedule_update_ha_state()
