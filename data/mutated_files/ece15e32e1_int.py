from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def __tmp4(__tmp8, config):
    """Set up the Route53 component."""
    __tmp6 = config[DOMAIN][CONF_DOMAIN]
    records = config[DOMAIN][CONF_RECORDS]
    __tmp2 = config[DOMAIN][CONF_ZONE]
    __tmp10 = config[DOMAIN][CONF_ACCESS_KEY_ID]
    __tmp5 = config[DOMAIN][CONF_SECRET_ACCESS_KEY]
    __tmp0 = config[DOMAIN][CONF_TTL]

    def __tmp3(__tmp9):
        """Set up recurring update."""
        __tmp7(
            __tmp10,
            __tmp5,
            __tmp2,
            __tmp6,
            records,
            __tmp0
        )

    def __tmp1(__tmp9):
        """Set up service for manual trigger."""
        __tmp7(
            __tmp10,
            __tmp5,
            __tmp2,
            __tmp6,
            records,
            __tmp0
        )

    track_time_interval(__tmp8, __tmp3, INTERVAL)

    __tmp8.services.register(DOMAIN, 'update_records', __tmp1)
    return True


def __tmp7(
        __tmp10,
        __tmp5,
        __tmp2,
        __tmp6,
        records,
        __tmp0: <FILL>,
):
    import boto3
    from ipify import get_ip
    from ipify import exceptions

    _LOGGER.debug("Starting update for zone %s", __tmp2)

    client = boto3.client(
        DOMAIN,
        __tmp10=__tmp10,
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
    for record in records:
        _LOGGER.debug("Processing record: %s", record)

        changes.append({
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': '{}.{}'.format(record, __tmp6),
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
        HostedZoneId=__tmp2, ChangeBatch={'Changes': changes})
    _LOGGER.debug("Response is %s", response)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        _LOGGER.warning(response)
