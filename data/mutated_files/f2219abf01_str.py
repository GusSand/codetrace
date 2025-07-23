"""IHC switch platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.ihc/
"""
from homeassistant.components.ihc import (
    IHC_DATA, IHC_CONTROLLER, IHC_INFO)
from homeassistant.components.ihc.ihcdevice import IHCDevice
from homeassistant.components.switch import SwitchDevice

DEPENDENCIES = ['ihc']


def __tmp1(__tmp4, config, add_entities, discovery_info=None):
    """Set up the IHC switch platform."""
    if discovery_info is None:
        return
    devices = []
    for name, device in discovery_info.items():
        ihc_id = device['ihc_id']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        __tmp5 = __tmp4.data[ihc_key][IHC_INFO]
        ihc_controller = __tmp4.data[ihc_key][IHC_CONTROLLER]

        switch = __typ0(ihc_controller, name, ihc_id, __tmp5, product)
        devices.append(switch)
    add_entities(devices)


class __typ0(IHCDevice, SwitchDevice):
    """IHC Switch."""

    def __init__(__tmp0, ihc_controller, name: <FILL>, ihc_id,
                 __tmp5, product=None) :
        """Initialize the IHC switch."""
        super().__init__(ihc_controller, name, ihc_id, product)
        __tmp0._state = False

    @property
    def is_on(__tmp0):
        """Return true if switch is on."""
        return __tmp0._state

    def turn_on(__tmp0, **kwargs):
        """Turn the switch on."""
        __tmp0.ihc_controller.set_runtime_value_bool(__tmp0.ihc_id, True)

    def turn_off(__tmp0, **kwargs):
        """Turn the device off."""
        __tmp0.ihc_controller.set_runtime_value_bool(__tmp0.ihc_id, False)

    def __tmp3(__tmp0, ihc_id, __tmp2):
        """Handle IHC resource change."""
        __tmp0._state = __tmp2
        __tmp0.schedule_update_ha_state()
