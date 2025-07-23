"""IHC switch platform.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.ihc/
"""
from homeassistant.components.ihc import (
    IHC_DATA, IHC_CONTROLLER, IHC_INFO)
from homeassistant.components.ihc.ihcdevice import IHCDevice
from homeassistant.components.switch import SwitchDevice

DEPENDENCIES = ['ihc']


def __tmp2(__tmp8, __tmp5, add_entities, discovery_info=None):
    """Set up the IHC switch platform."""
    if discovery_info is None:
        return
    devices = []
    for __tmp9, device in discovery_info.items():
        ihc_id = device['ihc_id']
        product = device['product']
        # Find controller that corresponds with device id
        ctrl_id = device['ctrl_id']
        ihc_key = IHC_DATA.format(ctrl_id)
        __tmp0 = __tmp8.data[ihc_key][IHC_INFO]
        ihc_controller = __tmp8.data[ihc_key][IHC_CONTROLLER]

        switch = IHCSwitch(ihc_controller, __tmp9, ihc_id, __tmp0, product)
        devices.append(switch)
    add_entities(devices)


class IHCSwitch(IHCDevice, SwitchDevice):
    """IHC Switch."""

    def __init__(__tmp1, ihc_controller, __tmp9, ihc_id,
                 __tmp0: <FILL>, product=None) :
        """Initialize the IHC switch."""
        super().__init__(ihc_controller, __tmp9, ihc_id, product)
        __tmp1._state = False

    @property
    def __tmp7(__tmp1):
        """Return true if switch is on."""
        return __tmp1._state

    def __tmp6(__tmp1, **kwargs):
        """Turn the switch on."""
        __tmp1.ihc_controller.set_runtime_value_bool(__tmp1.ihc_id, True)

    def __tmp4(__tmp1, **kwargs):
        """Turn the device off."""
        __tmp1.ihc_controller.set_runtime_value_bool(__tmp1.ihc_id, False)

    def on_ihc_change(__tmp1, ihc_id, __tmp3):
        """Handle IHC resource change."""
        __tmp1._state = __tmp3
        __tmp1.schedule_update_ha_state()
