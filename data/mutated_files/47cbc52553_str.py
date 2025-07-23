from typing import TypeAlias
__typ0 : TypeAlias = "int"
"""
Update the IP addresses of your Route53 DNS records.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/route53/
"""
from datetime import timedelta
import logging
from typing import List

import voluptuous as vol

from homeassistant.const import CONF_DOMAIN, CONF_TTL, CONF_ZONE
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_time_interval

REQUIREMENTS = ['boto3==1.9.16', 'ipify==1.0.0']

_LOGGER = logging.getLogger(__name__)

CONF_ACCESS_KEY_ID = 'aws_access_key_id'
CONF_SECRET_ACCESS_KEY = 'aws_secret_access_key'
CONF_RECORDS = 'records'

DOMAIN = 'route53'

INTERVAL = timedelta(minutes=60)
DEFAULT_TTL = 300

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_ACCESS_KEY_ID): cv.string,
        vol.Required(CONF_DOMAIN): cv.string,
        vol.Required(CONF_RECORDS): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(CONF_SECRET_ACCESS_KEY): cv.string,
        vol.Required(CONF_ZONE): cv.string,
        vol.Optional(CONF_TTL, default=DEFAULT_TTL): cv.positive_int,
    })
}, extra=vol.ALLOW_EXTRA)


def __tmp4(__tmp9, config):
    """Set up the Route53 component."""
    __tmp8 = config[DOMAIN][CONF_DOMAIN]
    __tmp6 = config[DOMAIN][CONF_RECORDS]
    __tmp3 = config[DOMAIN][CONF_ZONE]
    __tmp11 = config[DOMAIN][CONF_ACCESS_KEY_ID]
    __tmp5 = config[DOMAIN][CONF_SECRET_ACCESS_KEY]
    __tmp0 = config[DOMAIN][CONF_TTL]

    def __tmp2(__tmp10):
        """Set up recurring update."""
        __tmp7(
            __tmp11,
            __tmp5,
            __tmp3,
            __tmp8,
            __tmp6,
            __tmp0
        )

    def __tmp1(__tmp10):
        """Set up service for manual trigger."""
        __tmp7(
            __tmp11,
            __tmp5,
            __tmp3,
            __tmp8,
            __tmp6,
            __tmp0
        )

    track_time_interval(__tmp9, __tmp2, INTERVAL)

    __tmp9.services.register(DOMAIN, 'update_records', __tmp1)
    return True


def __tmp7(
        __tmp11: <FILL>,
        __tmp5,
        __tmp3,
        __tmp8,
        __tmp6,
        __tmp0: __typ0,
):
    import boto3
    from ipify import get_ip
    from ipify import exceptions

    _LOGGER.debug("Starting update for zone %s", __tmp3)

    client = boto3.client(
        DOMAIN,
        __tmp11=__tmp11,
        __tmp5=__tmp5,
    )

    # Get the IP Address and build an array of changes
    try:
        ipaddress = get_ip()

    except exceptions.ConnectionError:
        _LOGGER.warning("Unable to reach the ipify service")
        return

    except exceptions.ServiceError:
        _LOGGER.warning("Unable to complete the ipfy request")
        return

    changes = []
    for record in __tmp6:
        _LOGGER.debug("Processing record: %s", record)

        changes.append({
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': '{}.{}'.format(record, __tmp8),
                'Type': 'A',
                'TTL': __tmp0,
                'ResourceRecords': [
                    {'Value': ipaddress},
                ],
            }
        })

    _LOGGER.debug("Submitting the following changes to Route53")
    _LOGGER.debug(changes)

    response = client.change_resource_record_sets(
        HostedZoneId=__tmp3, ChangeBatch={'Changes': changes})
    _LOGGER.debug("Response is %s", response)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        _LOGGER.warning(response)
