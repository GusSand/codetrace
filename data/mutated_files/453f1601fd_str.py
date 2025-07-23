"""
Support for Huawei LTE routers.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/huawei_lte/
"""
from datetime import timedelta
from functools import reduce
import logging
import operator

import voluptuous as vol
import attr

from homeassistant.const import (
    CONF_URL, CONF_USERNAME, CONF_PASSWORD, EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.util import Throttle


_LOGGER = logging.getLogger(__name__)

# dicttoxml (used by huawei-lte-api) has uselessly verbose INFO level.
# https://github.com/quandyfactory/dicttoxml/issues/60
logging.getLogger('dicttoxml').setLevel(logging.WARNING)

REQUIREMENTS = ['huawei-lte-api==1.1.3']

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

DOMAIN = 'huawei_lte'
DATA_KEY = 'huawei_lte'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.All(cv.ensure_list, [vol.Schema({
        vol.Required(CONF_URL): cv.url,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    })])
}, extra=vol.ALLOW_EXTRA)


@attr.s
class RouterData:
    """Class for router state."""

    client = attr.ib()
    device_information = attr.ib(init=False, factory=dict)
    device_signal = attr.ib(init=False, factory=dict)
    traffic_statistics = attr.ib(init=False, factory=dict)
    wlan_host_list = attr.ib(init=False, factory=dict)

    _subscriptions = attr.ib(init=False, factory=set)

    def __tmp7(__tmp1) :
        """Fetch device information once, for serial number in @unique_ids."""
        __tmp1.subscribe("device_information")
        __tmp1._update()
        __tmp1.unsubscribe("device_information")

    def __tmp0(__tmp1, __tmp4: <FILL>):
        """
        Get value corresponding to a dotted path.

        The first path component designates a member of this class
        such as device_information, device_signal etc, and the remaining
        path points to a value in the member's data structure.
        """
        root, *rest = __tmp4.split(".")
        try:
            data = getattr(__tmp1, root)
        except AttributeError as err:
            raise KeyError from err
        return reduce(operator.getitem, rest, data)

    def subscribe(__tmp1, __tmp4) :
        """Subscribe to given router data entries."""
        __tmp1._subscriptions.add(__tmp4.split(".")[0])

    def unsubscribe(__tmp1, __tmp4: str) :
        """Unsubscribe from given router data entries."""
        __tmp1._subscriptions.discard(__tmp4.split(".")[0])

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def __tmp10(__tmp1) -> None:
        """Call API to update data."""
        __tmp1._update()

    def _update(__tmp1) :
        debugging = _LOGGER.isEnabledFor(logging.DEBUG)
        if debugging or "device_information" in __tmp1._subscriptions:
            __tmp1.device_information = __tmp1.client.device.information()
            _LOGGER.debug("device_information=%s", __tmp1.device_information)
        if debugging or "device_signal" in __tmp1._subscriptions:
            __tmp1.device_signal = __tmp1.client.device.signal()
            _LOGGER.debug("device_signal=%s", __tmp1.device_signal)
        if debugging or "traffic_statistics" in __tmp1._subscriptions:
            __tmp1.traffic_statistics = \
                __tmp1.client.monitoring.traffic_statistics()
            _LOGGER.debug("traffic_statistics=%s", __tmp1.traffic_statistics)
        if debugging or "wlan_host_list" in __tmp1._subscriptions:
            __tmp1.wlan_host_list = __tmp1.client.wlan.host_list()
            _LOGGER.debug("wlan_host_list=%s", __tmp1.wlan_host_list)


@attr.s
class HuaweiLteData:
    """Shared state."""

    data = attr.ib(init=False, factory=dict)

    def __tmp2(__tmp1, config):
        """Get the requested or the only data value."""
        if CONF_URL in config:
            return __tmp1.data.get(config[CONF_URL])
        if len(__tmp1.data) == 1:
            return next(iter(__tmp1.data.values()))

        return None


def __tmp6(__tmp8, config) :
    """Set up Huawei LTE component."""
    if DATA_KEY not in __tmp8.data:
        __tmp8.data[DATA_KEY] = HuaweiLteData()
    for conf in config.get(DOMAIN, []):
        __tmp5(__tmp8, conf)
    return True


def __tmp5(__tmp8, __tmp9) :
    """Set up Huawei LTE router."""
    from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
    from huawei_lte_api.Client import Client

    url = __tmp9[CONF_URL]
    username = __tmp9[CONF_USERNAME]
    password = __tmp9[CONF_PASSWORD]

    connection = AuthorizedConnection(
        url,
        username=username,
        password=password,
    )
    client = Client(connection)

    data = RouterData(client)
    __tmp8.data[DATA_KEY].data[url] = data

    def __tmp11(__tmp3):
        """Clean up resources."""
        client.user.logout()

    __tmp8.bus.listen_once(EVENT_HOMEASSISTANT_STOP, __tmp11)
