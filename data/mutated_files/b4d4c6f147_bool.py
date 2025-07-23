from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""IHC light platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.ihc/
"""
import logging

from homeassistant.components.ihc import (
    IHC_DATA, IHC_CONTROLLER, IHC_INFO)
from homeassistant.components.ihc.const import (
    CONF_DIMMABLE)
from homeassistant.components.ihc.ihcdevice import IHCDevice
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light)

DEPENDENCIES = ['ihc']

_LOGGER = logging.getLogger(__name__)


def setup_platform(__tmp9, __tmp6, __tmp2, discovery_info=None):
    """Set up the IHC lights platform."""
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
        __tmp11 = __tmp9.data[ihc_key][IHC_INFO]
        ihc_controller = __tmp9.data[ihc_key][IHC_CONTROLLER]
        dimmable = product_cfg[CONF_DIMMABLE]
        light = __typ1(ihc_controller, __tmp3, ihc_id, __tmp11,
                         dimmable, product)
        devices.append(light)
    __tmp2(devices)


class __typ1(IHCDevice, Light):
    """Representation of a IHC light.

    For dimmable lights, the associated IHC resource should be a light
    level (integer). For non dimmable light the IHC resource should be
    an on/off (boolean) resource
    """

    def __init__(__tmp1, ihc_controller, __tmp3, ihc_id, __tmp11: <FILL>,
                 dimmable=False, product=None) :
        """Initialize the light."""
        super().__init__(ihc_controller, __tmp3, ihc_id, __tmp11, product)
        __tmp1._brightness = 0
        __tmp1._dimmable = dimmable
        __tmp1._state = None

    @property
    def __tmp0(__tmp1) :
        """Return the brightness of this light between 0..255."""
        return __tmp1._brightness

    @property
    def __tmp8(__tmp1) :
        """Return true if light is on."""
        return __tmp1._state

    @property
    def __tmp10(__tmp1):
        """Flag supported features."""
        if __tmp1._dimmable:
            return SUPPORT_BRIGHTNESS
        return 0

    def __tmp7(__tmp1, **kwargs) :
        """Turn the light on."""
        if ATTR_BRIGHTNESS in kwargs:
            __tmp0 = kwargs[ATTR_BRIGHTNESS]
        else:
            __tmp0 = __tmp1._brightness
            if __tmp0 == 0:
                __tmp0 = 255

        if __tmp1._dimmable:
            __tmp1.ihc_controller.set_runtime_value_int(
                __tmp1.ihc_id, __typ0(__tmp0 * 100 / 255))
        else:
            __tmp1.ihc_controller.set_runtime_value_bool(__tmp1.ihc_id, True)

    def turn_off(__tmp1, **kwargs) :
        """Turn the light off."""
        if __tmp1._dimmable:
            __tmp1.ihc_controller.set_runtime_value_int(__tmp1.ihc_id, 0)
        else:
            __tmp1.ihc_controller.set_runtime_value_bool(__tmp1.ihc_id, False)

    def __tmp5(__tmp1, ihc_id, __tmp4):
        """Handle IHC notifications."""
        if isinstance(__tmp4, bool):
            __tmp1._dimmable = False
            __tmp1._state = __tmp4 != 0
        else:
            __tmp1._dimmable = True
            __tmp1._state = __tmp4 > 0
            if __tmp1._state:
                __tmp1._brightness = __typ0(__tmp4 * 255 / 100)
        __tmp1.schedule_update_ha_state()
