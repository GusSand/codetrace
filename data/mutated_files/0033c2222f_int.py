from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the IHC lights platform."""
    if discovery_info is None:
        return
    devices = []
    for name, device in discovery_info.items():
        ihc_id = device['ihc_id']
        product_cfg = device['product_cfg']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        info = hass.data[ihc_key][IHC_INFO]
        ihc_controller = hass.data[ihc_key][IHC_CONTROLLER]
        dimmable = product_cfg[CONF_DIMMABLE]
        light = IhcLight(ihc_controller, name, ihc_id, info,
                         dimmable, product)
        devices.append(light)
    add_entities(devices)


class IhcLight(IHCDevice, Light):
    """Representation of a IHC light.

    For dimmable lights, the associated IHC resource should be a light
    level (integer). For non dimmable light the IHC resource should be
    an on/off (boolean) resource
    """

    def __init__(__tmp0, ihc_controller, name, ihc_id: <FILL>, info,
                 dimmable=False, product=None) :
        """Initialize the light."""
        super().__init__(ihc_controller, name, ihc_id, info, product)
        __tmp0._brightness = 0
        __tmp0._dimmable = dimmable
        __tmp0._state = None

    @property
    def brightness(__tmp0) -> int:
        """Return the brightness of this light between 0..255."""
        return __tmp0._brightness

    @property
    def is_on(__tmp0) :
        """Return true if light is on."""
        return __tmp0._state

    @property
    def supported_features(__tmp0):
        """Flag supported features."""
        if __tmp0._dimmable:
            return SUPPORT_BRIGHTNESS
        return 0

    def turn_on(__tmp0, **kwargs) :
        """Turn the light on."""
        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs[ATTR_BRIGHTNESS]
        else:
            brightness = __tmp0._brightness
            if brightness == 0:
                brightness = 255

        if __tmp0._dimmable:
            __tmp0.ihc_controller.set_runtime_value_int(
                __tmp0.ihc_id, int(brightness * 100 / 255))
        else:
            __tmp0.ihc_controller.set_runtime_value_bool(__tmp0.ihc_id, True)

    def turn_off(__tmp0, **kwargs) :
        """Turn the light off."""
        if __tmp0._dimmable:
            __tmp0.ihc_controller.set_runtime_value_int(__tmp0.ihc_id, 0)
        else:
            __tmp0.ihc_controller.set_runtime_value_bool(__tmp0.ihc_id, False)

    def on_ihc_change(__tmp0, ihc_id, value):
        """Handle IHC notifications."""
        if isinstance(value, __typ0):
            __tmp0._dimmable = False
            __tmp0._state = value != 0
        else:
            __tmp0._dimmable = True
            __tmp0._state = value > 0
            if __tmp0._state:
                __tmp0._brightness = int(value * 255 / 100)
        __tmp0.schedule_update_ha_state()
