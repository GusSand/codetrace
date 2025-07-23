from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "dict"
"""
Fans on Zigbee Home Automation networks.

For more details on this platform, please refer to the documentation
at https://home-assistant.io/components/fan.zha/
"""
import logging

from homeassistant.components.fan import (
    DOMAIN, SPEED_HIGH, SPEED_LOW, SPEED_MEDIUM, SPEED_OFF, SUPPORT_SET_SPEED,
    FanEntity)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from . import helpers
from .const import (
    DATA_ZHA, DATA_ZHA_DISPATCHERS, REPORT_CONFIG_OP, ZHA_DISCOVERY_NEW)
from .entities import ZhaEntity

DEPENDENCIES = ['zha']

_LOGGER = logging.getLogger(__name__)

# Additional speeds in zigbee's ZCL
# Spec is unclear as to what this value means. On King Of Fans HBUniversal
# receiver, this means Very High.
SPEED_ON = 'on'
# The fan speed is self-regulated
SPEED_AUTO = 'auto'
# When the heated/cooled space is occupied, the fan is always on
SPEED_SMART = 'smart'

SPEED_LIST = [
    SPEED_OFF,
    SPEED_LOW,
    SPEED_MEDIUM,
    SPEED_HIGH,
    SPEED_ON,
    SPEED_AUTO,
    SPEED_SMART
]

VALUE_TO_SPEED = {i: speed for i, speed in enumerate(SPEED_LIST)}
SPEED_TO_VALUE = {speed: i for i, speed in enumerate(SPEED_LIST)}


async def async_setup_platform(__tmp14, config, __tmp1,
                               __tmp8=None):
    """Old way of setting up Zigbee Home Automation fans."""
    pass


async def __tmp0(__tmp14, __tmp17, __tmp1):
    """Set up the Zigbee Home Automation fan from config entry."""
    async def __tmp7(__tmp8):
        await __tmp3(__tmp14, __tmp17, __tmp1,
                                    [__tmp8])

    unsub = async_dispatcher_connect(
        __tmp14, ZHA_DISCOVERY_NEW.format(DOMAIN), __tmp7)
    __tmp14.data[DATA_ZHA][DATA_ZHA_DISPATCHERS].append(unsub)

    fans = __tmp14.data.get(DATA_ZHA, {}).get(DOMAIN)
    if fans is not None:
        await __tmp3(__tmp14, __tmp17, __tmp1,
                                    fans.values())
        del __tmp14.data[DATA_ZHA][DOMAIN]


async def __tmp3(__tmp14, __tmp17, __tmp1,
                                __tmp6):
    """Set up the ZHA fans."""
    entities = []
    for __tmp8 in __tmp6:
        entities.append(__typ0(**__tmp8))

    __tmp1(entities, update_before_add=True)


class __typ0(ZhaEntity, FanEntity):
    """Representation of a ZHA fan."""

    _domain = DOMAIN
    value_attribute = 0  # fan_mode

    @property
    def __tmp9(__tmp2) -> __typ1:
        """Return a dict of attribute reporting configuration."""
        return {
            __tmp2.cluster: {__tmp2.value_attribute: REPORT_CONFIG_OP}
        }

    @property
    def cluster(__tmp2):
        """Fan ZCL Cluster."""
        return __tmp2._endpoint.fan

    @property
    def __tmp16(__tmp2) -> int:
        """Flag supported features."""
        return SUPPORT_SET_SPEED

    @property
    def __tmp13(__tmp2) -> list:
        """Get the list of available speeds."""
        return SPEED_LIST

    @property
    def speed(__tmp2) -> str:
        """Return the current speed."""
        return __tmp2._state

    @property
    def __tmp12(__tmp2) -> __typ2:
        """Return true if entity is on."""
        if __tmp2._state is None:
            return False
        return __tmp2._state != SPEED_OFF

    async def async_turn_on(__tmp2, speed: str = None, **kwargs) :
        """Turn the entity on."""
        if speed is None:
            speed = SPEED_MEDIUM

        await __tmp2.async_set_speed(speed)

    async def __tmp10(__tmp2, **kwargs) :
        """Turn the entity off."""
        await __tmp2.async_set_speed(SPEED_OFF)

    async def async_set_speed(__tmp2, speed: <FILL>) -> None:
        """Set the speed of the fan."""
        from zigpy.exceptions import DeliveryError
        try:
            await __tmp2._endpoint.fan.write_attributes(
                {'fan_mode': SPEED_TO_VALUE[speed]}
            )
        except DeliveryError as ex:
            _LOGGER.error("%s: Could not set speed: %s", __tmp2.entity_id, ex)
            return

        __tmp2._state = speed
        __tmp2.async_schedule_update_ha_state()

    async def __tmp11(__tmp2):
        """Retrieve latest state."""
        result = await helpers.safe_read(__tmp2.cluster, ['fan_mode'],
                                         allow_cache=False,
                                         only_cache=(not __tmp2._initialized))
        new_value = result.get('fan_mode', None)
        __tmp2._state = VALUE_TO_SPEED.get(new_value, None)

    def __tmp15(__tmp2, __tmp5, __tmp4):
        """Handle attribute update from device."""
        attr_name = __tmp2.cluster.attributes.get(__tmp5, [__tmp5])[0]
        _LOGGER.debug("%s: Attribute report '%s'[%s] = %s",
                      __tmp2.entity_id, __tmp2.cluster.name, attr_name, __tmp4)
        if __tmp5 == __tmp2.value_attribute:
            __tmp2._state = VALUE_TO_SPEED.get(__tmp4, __tmp2._state)
            __tmp2.async_schedule_update_ha_state()
