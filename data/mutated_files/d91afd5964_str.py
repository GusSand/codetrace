"""
Support for Huawei LTE routers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.huawei_lte/
"""
from typing import Any, Dict, List, Optional

import attr
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import (
    PLATFORM_SCHEMA, DeviceScanner,
)
from homeassistant.const import CONF_URL
from ..huawei_lte import DATA_KEY, RouterData


DEPENDENCIES = ['huawei_lte']

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_URL): cv.url,
})

HOSTS_PATH = "wlan_host_list.Hosts"


def get_scanner(__tmp0, config):
    """Get a Huawei LTE router scanner."""
    data = __tmp0.data[DATA_KEY].get_data(config)
    data.subscribe(HOSTS_PATH)
    return HuaweiLteScanner(data)


@attr.s
class HuaweiLteScanner(DeviceScanner):
    """Huawei LTE router scanner."""

    data = attr.ib(type=RouterData)

    _hosts = attr.ib(init=False, factory=dict)

    def scan_devices(__tmp1) :
        """Scan for devices."""
        __tmp1.data.update()
        __tmp1._hosts = {
            x["MacAddress"]: x
            for x in __tmp1.data[HOSTS_PATH + ".Host"]
            if x.get("MacAddress")
        }
        return list(__tmp1._hosts)

    def __tmp3(__tmp1, device) :
        """Get name for a device."""
        host = __tmp1._hosts.get(device)
        return host.get("HostName") or None if host else None

    def __tmp2(__tmp1, device: <FILL>) :
        """
        Get extra attributes of a device.

        Some known extra attributes that may be returned in the dict
        include MacAddress (MAC address), ID (client ID), IpAddress
        (IP address), AssociatedSsid (associated SSID), AssociatedTime
        (associated time in seconds), and HostName (host name).
        """
        return __tmp1._hosts.get(device) or {}
