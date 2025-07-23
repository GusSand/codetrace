from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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


def setup_platform(hass, __tmp2, __tmp1, discovery_info=None):
    """Set up the IHC sensor platform."""
    if discovery_info is None:
        return
    devices = []
    for __tmp3, device in discovery_info.items():
        ihc_id = device['ihc_id']
        product_cfg = device['product_cfg']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        info = hass.data[ihc_key][IHC_INFO]
        ihc_controller = hass.data[ihc_key][IHC_CONTROLLER]
        unit = product_cfg[CONF_UNIT_OF_MEASUREMENT]
        sensor = __typ1(ihc_controller, __tmp3, ihc_id, info,
                           unit, product)
        devices.append(sensor)
    __tmp1(devices)


class __typ1(IHCDevice, Entity):
    """Implementation of the IHC sensor."""

    def __init__(__tmp0, ihc_controller, __tmp3, ihc_id: <FILL>, info,
                 unit, product=None) :
        """Initialize the IHC sensor."""
        super().__init__(ihc_controller, __tmp3, ihc_id, info, product)
        __tmp0._state = None
        __tmp0._unit_of_measurement = unit

    @property
    def state(__tmp0):
        """Return the state of the sensor."""
        return __tmp0._state

    @property
    def unit_of_measurement(__tmp0):
        """Return the unit of measurement of this entity, if any."""
        return __tmp0._unit_of_measurement

    def on_ihc_change(__tmp0, ihc_id, value):
        """Handle IHC resource change."""
        __tmp0._state = value
        __tmp0.schedule_update_ha_state()
