from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""IHC binary sensor platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/binary_sensor.ihc/
"""
from homeassistant.components.binary_sensor import (
    BinarySensorDevice)
from homeassistant.components.ihc import (
    IHC_DATA, IHC_CONTROLLER, IHC_INFO)
from homeassistant.components.ihc.const import (
    CONF_INVERTING)
from homeassistant.components.ihc.ihcdevice import IHCDevice
from homeassistant.const import (
    CONF_TYPE)

DEPENDENCIES = ['ihc']


def __tmp2(hass, __tmp5, __tmp1, discovery_info=None):
    """Set up the IHC binary sensor platform."""
    if discovery_info is None:
        return
    devices = []
    for __tmp8, device in discovery_info.items():
        __tmp4 = device['ihc_id']
        product_cfg = device['product_cfg']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        info = hass.data[ihc_key][IHC_INFO]
        __tmp7 = hass.data[ihc_key][IHC_CONTROLLER]

        sensor = __typ1(__tmp7, __tmp8, __tmp4, info,
                                 product_cfg.get(CONF_TYPE),
                                 product_cfg[CONF_INVERTING],
                                 product)
        devices.append(sensor)
    __tmp1(devices)


class __typ1(IHCDevice, BinarySensorDevice):
    """IHC Binary Sensor.

    The associated IHC resource can be any in or output from a IHC product
    or function block, but it must be a boolean ON/OFF resources.
    """

    def __init__(__tmp0, __tmp7, __tmp8, __tmp4: <FILL>, info,
                 sensor_type, inverting,
                 product=None) :
        """Initialize the IHC binary sensor."""
        super().__init__(__tmp7, __tmp8, __tmp4, info, product)
        __tmp0._state = None
        __tmp0._sensor_type = sensor_type
        __tmp0.inverting = inverting

    @property
    def device_class(__tmp0):
        """Return the class of this sensor."""
        return __tmp0._sensor_type

    @property
    def __tmp6(__tmp0):
        """Return true if the binary sensor is on/open."""
        return __tmp0._state

    def on_ihc_change(__tmp0, __tmp4, __tmp3):
        """IHC resource has changed."""
        if __tmp0.inverting:
            __tmp0._state = not __tmp3
        else:
            __tmp0._state = __tmp3
        __tmp0.schedule_update_ha_state()
