from typing import TypeAlias
__typ0 : TypeAlias = "ArmingState"
"""
Support for Ness D8X/D16X devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/ness_alarm/
"""
import logging
from collections import namedtuple

import voluptuous as vol

from homeassistant.components.binary_sensor import DEVICE_CLASSES
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send

REQUIREMENTS = ['nessclient==0.9.9']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'ness_alarm'
DATA_NESS = 'ness_alarm'

CONF_DEVICE_HOST = 'host'
CONF_DEVICE_PORT = 'port'
CONF_ZONES = 'zones'
CONF_ZONE_NAME = 'name'
CONF_ZONE_TYPE = 'type'
CONF_ZONE_ID = 'id'
ATTR_CODE = 'code'
ATTR_OUTPUT_ID = 'output_id'
ATTR_STATE = 'state'
DEFAULT_ZONES = []

SIGNAL_ZONE_CHANGED = 'ness_alarm.zone_changed'
SIGNAL_ARMING_STATE_CHANGED = 'ness_alarm.arming_state_changed'

ZoneChangedData = namedtuple('ZoneChangedData', ['zone_id', 'state'])

DEFAULT_ZONE_TYPE = 'motion'
ZONE_SCHEMA = vol.Schema({
    vol.Required(CONF_ZONE_NAME): cv.string,
    vol.Required(CONF_ZONE_ID): cv.positive_int,
    vol.Optional(CONF_ZONE_TYPE, default=DEFAULT_ZONE_TYPE):
        vol.In(DEVICE_CLASSES)})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICE_HOST): cv.string,
        vol.Required(CONF_DEVICE_PORT): cv.port,
        vol.Optional(CONF_ZONES, default=DEFAULT_ZONES):
            vol.All(cv.ensure_list, [ZONE_SCHEMA]),
    }),
}, extra=vol.ALLOW_EXTRA)

SERVICE_PANIC = 'panic'
SERVICE_AUX = 'aux'

SERVICE_SCHEMA_PANIC = vol.Schema({
    vol.Required(ATTR_CODE): cv.string,
})
SERVICE_SCHEMA_AUX = vol.Schema({
    vol.Required(ATTR_OUTPUT_ID): cv.positive_int,
    vol.Optional(ATTR_STATE, default=True): cv.boolean,
})


async def async_setup(__tmp6, config):
    """Set up the Ness Alarm platform."""
    from nessclient import Client, ArmingState
    conf = config[DOMAIN]

    zones = conf[CONF_ZONES]
    host = conf[CONF_DEVICE_HOST]
    port = conf[CONF_DEVICE_PORT]

    client = Client(host=host, port=port, loop=__tmp6.loop)
    __tmp6.data[DATA_NESS] = client

    async def __tmp0(__tmp2):
        await client.close()

    __tmp6.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, __tmp0)

    __tmp6.async_create_task(
        async_load_platform(__tmp6, 'binary_sensor', DOMAIN, {CONF_ZONES: zones},
                            config))
    __tmp6.async_create_task(
        async_load_platform(__tmp6, 'alarm_control_panel', DOMAIN, {}, config))

    def on_zone_change(__tmp1: <FILL>, __tmp3):
        """Receives and propagates zone state updates."""
        async_dispatcher_send(__tmp6, SIGNAL_ZONE_CHANGED, ZoneChangedData(
            __tmp1=__tmp1,
            __tmp3=__tmp3,
        ))

    def on_state_change(__tmp4: __typ0):
        """Receives and propagates arming state updates."""
        async_dispatcher_send(__tmp6, SIGNAL_ARMING_STATE_CHANGED, __tmp4)

    client.on_zone_change(on_zone_change)
    client.on_state_change(on_state_change)

    # Force update for current arming status and current zone states
    __tmp6.loop.create_task(client.keepalive())
    __tmp6.loop.create_task(client.update())

    async def handle_panic(__tmp5):
        await client.panic(__tmp5.data[ATTR_CODE])

    async def handle_aux(__tmp5):
        await client.aux(__tmp5.data[ATTR_OUTPUT_ID], __tmp5.data[ATTR_STATE])

    __tmp6.services.async_register(DOMAIN, SERVICE_PANIC, handle_panic,
                                 schema=SERVICE_SCHEMA_PANIC)
    __tmp6.services.async_register(DOMAIN, SERVICE_AUX, handle_aux,
                                 schema=SERVICE_SCHEMA_AUX)

    return True
