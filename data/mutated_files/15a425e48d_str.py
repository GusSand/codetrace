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


def setup_platform(hass, __tmp4, add_entities, discovery_info=None):
    """Set up the IHC binary sensor platform."""
    if discovery_info is None:
        return
    devices = []
    for name, device in discovery_info.items():
        __tmp2 = device['ihc_id']
        product_cfg = device['product_cfg']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        __tmp7 = hass.data[ihc_key][IHC_INFO]
        __tmp6 = hass.data[ihc_key][IHC_CONTROLLER]

        sensor = __typ0(__tmp6, name, __tmp2, __tmp7,
                                 product_cfg.get(CONF_TYPE),
                                 product_cfg[CONF_INVERTING],
                                 product)
        devices.append(sensor)
    add_entities(devices)


class __typ0(IHCDevice, BinarySensorDevice):
    """IHC Binary Sensor.

    The associated IHC resource can be any in or output from a IHC product
    or function block, but it must be a boolean ON/OFF resources.
    """

    def __init__(__tmp0, __tmp6, name, __tmp2: int, __tmp7,
                 sensor_type: <FILL>, inverting: bool,
                 product=None) :
        """Initialize the IHC binary sensor."""
        super().__init__(__tmp6, name, __tmp2, __tmp7, product)
        __tmp0._state = None
        __tmp0._sensor_type = sensor_type
        __tmp0.inverting = inverting

    @property
    def device_class(__tmp0):
        """Return the class of this sensor."""
        return __tmp0._sensor_type

    @property
    def __tmp5(__tmp0):
        """Return true if the binary sensor is on/open."""
        return __tmp0._state

    def __tmp3(__tmp0, __tmp2, __tmp1):
        """IHC resource has changed."""
        if __tmp0.inverting:
            __tmp0._state = not __tmp1
        else:
            __tmp0._state = __tmp1
        __tmp0.schedule_update_ha_state()
