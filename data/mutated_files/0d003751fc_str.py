from typing import TypeAlias
__typ0 : TypeAlias = "ToggleEntity"
__typ2 : TypeAlias = "list"
"""
Support for Insteon fans via local hub control.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/fan.insteon_local/
"""
import logging
from datetime import timedelta

from homeassistant.components.fan import (
    ATTR_SPEED, SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH,
    SUPPORT_SET_SPEED, FanEntity)
from homeassistant.helpers.entity import ToggleEntity
import homeassistant.util as util
from homeassistant.util.json import load_json, save_json

_CONFIGURING = {}
_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['insteon_local']
DOMAIN = 'fan'

INSTEON_LOCAL_FANS_CONF = 'insteon_local_fans.conf'

MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(milliseconds=100)
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=5)

SUPPORT_INSTEON_LOCAL = SUPPORT_SET_SPEED


def __tmp1(__tmp10, config, add_devices, discovery_info=None):
    """Set up the Insteon local fan platform."""
    __tmp9 = __tmp10.data['insteon_local']

    conf_fans = load_json(__tmp10.config.path(INSTEON_LOCAL_FANS_CONF))
    if conf_fans:
        for device_id in conf_fans:
            setup_fan(device_id, conf_fans[device_id], __tmp9, __tmp10,
                      add_devices)

    else:
        linked = __tmp9.get_linked()

        for device_id in linked:
            if (linked[device_id]['cat_type'] == 'dimmer' and
                    linked[device_id]['sku'] == '2475F' and
                    device_id not in conf_fans):
                __tmp3(device_id,
                                      __tmp9,
                                      linked[device_id]['model_name'] + ' ' +
                                      linked[device_id]['sku'],
                                      __tmp10, add_devices)


def __tmp3(device_id, __tmp9, __tmp4, __tmp10,
                          __tmp2):
    """Request configuration steps from the user."""
    configurator = __tmp10.components.configurator

    # We got an error if this method is called while we are configuring
    if device_id in _CONFIGURING:
        configurator.notify_errors(
            _CONFIGURING[device_id], 'Failed to register, please try again.')

        return

    def insteon_fan_config_callback(data):
        """The actions to do when our configuration callback is called."""
        setup_fan(device_id, data.get('name'), __tmp9, __tmp10,
                  __tmp2)

    _CONFIGURING[device_id] = configurator.request_config(
        'Insteon  ' + __tmp4 + ' addr: ' + device_id,
        insteon_fan_config_callback,
        description=('Enter a name for ' + __tmp4 + ' Fan addr: ' + device_id),
        entity_picture='/static/images/config_insteon.png',
        submit_caption='Confirm',
        fields=[{'id': 'name', 'name': 'Name', 'type': ''}]
    )


def setup_fan(device_id, __tmp11, __tmp9, __tmp10, __tmp2):
    """Set up the fan."""
    if device_id in _CONFIGURING:
        request_id = _CONFIGURING.pop(device_id)
        configurator = __tmp10.components.configurator
        configurator.request_done(request_id)
        _LOGGER.info("Device configuration done!")

    conf_fans = load_json(__tmp10.config.path(INSTEON_LOCAL_FANS_CONF))
    if device_id not in conf_fans:
        conf_fans[device_id] = __tmp11

    save_json(__tmp10.config.path(INSTEON_LOCAL_FANS_CONF), conf_fans)

    device = __tmp9.fan(device_id)
    __tmp2([__typ1(device, __tmp11)])


class __typ1(FanEntity):
    """An abstract Class for an Insteon node."""

    def __init__(__tmp0, node, __tmp11):
        """Initialize the device."""
        __tmp0.node = node
        __tmp0.node.deviceName = __tmp11
        __tmp0._speed = SPEED_OFF

    @property
    def __tmp11(__tmp0):
        """Return the name of the node."""
        return __tmp0.node.deviceName

    @property
    def unique_id(__tmp0):
        """Return the ID of this Insteon node."""
        return 'insteon_local_{}_fan'.format(__tmp0.node.device_id)

    @property
    def __tmp6(__tmp0) :
        """Return the current speed."""
        return __tmp0._speed

    @property
    def __tmp8(__tmp0) -> __typ2:
        """Get the list of available speeds."""
        return [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def __tmp5(__tmp0):
        """Update state of the fan."""
        resp = __tmp0.node.status()
        if 'cmd2' in resp:
            if resp['cmd2'] == '00':
                __tmp0._speed = SPEED_OFF
            elif resp['cmd2'] == '55':
                __tmp0._speed = SPEED_LOW
            elif resp['cmd2'] == 'AA':
                __tmp0._speed = SPEED_MEDIUM
            elif resp['cmd2'] == 'FF':
                __tmp0._speed = SPEED_HIGH

    @property
    def supported_features(__tmp0):
        """Flag supported features."""
        return SUPPORT_INSTEON_LOCAL

    def __tmp7(__tmp0, __tmp6: str=None, **kwargs) :
        """Turn device on."""
        if __tmp6 is None:
            if ATTR_SPEED in kwargs:
                __tmp6 = kwargs[ATTR_SPEED]
            else:
                __tmp6 = SPEED_MEDIUM

        __tmp0.set_speed(__tmp6)

    def turn_off(__tmp0: __typ0, **kwargs) -> None:
        """Turn device off."""
        __tmp0.node.off()

    def set_speed(__tmp0, __tmp6: <FILL>) :
        """Set the speed of the fan."""
        if __tmp0.node.on(__tmp6):
            __tmp0._speed = __tmp6
