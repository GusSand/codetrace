from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""IHC sensor platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.ihc/
"""
from homeassistant.components.ihc import (
    IHC_DATA, IHC_CONTROLLER, IHC_INFO)
from homeassistant.components.ihc.ihcdevice import IHCDevice
from homeassistant.const import (
    CONF_UNIT_OF_MEASUREMENT)
from homeassistant.helpers.entity import Entity

DEPENDENCIES = ['ihc']


def __tmp1(__tmp6, __tmp5, add_entities, discovery_info=None):
    """Set up the IHC sensor platform."""
    if discovery_info is None:
        return
    devices = []
    for __tmp7, device in discovery_info.items():
        __tmp2 = device['ihc_id']
        product_cfg = device['product_cfg']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        info = __tmp6.data[ihc_key][IHC_INFO]
        ihc_controller = __tmp6.data[ihc_key][IHC_CONTROLLER]
        unit = product_cfg[CONF_UNIT_OF_MEASUREMENT]
        sensor = IHCSensor(ihc_controller, __tmp7, __tmp2, info,
                           unit, product)
        devices.append(sensor)
    add_entities(devices)


class IHCSensor(IHCDevice, Entity):
    """Implementation of the IHC sensor."""

    def __init__(__tmp0, ihc_controller, __tmp7, __tmp2, info: <FILL>,
                 unit, product=None) -> None:
        """Initialize the IHC sensor."""
        super().__init__(ihc_controller, __tmp7, __tmp2, info, product)
        __tmp0._state = None
        __tmp0._unit_of_measurement = unit

    @property
    def state(__tmp0):
        """Return the state of the sensor."""
        return __tmp0._state

    @property
    def __tmp4(__tmp0):
        """Return the unit of measurement of this entity, if any."""
        return __tmp0._unit_of_measurement

    def __tmp3(__tmp0, __tmp2, value):
        """Handle IHC resource change."""
        __tmp0._state = value
        __tmp0.schedule_update_ha_state()
