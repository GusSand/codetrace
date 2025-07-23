"""Ban logic for HTTP component."""
import asyncio
from collections import defaultdict
from datetime import datetime
from ipaddress import ip_address
import logging
import os

from aiohttp.web import middleware
from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
import voluptuous as vol

from homeassistant.components import persistent_notification
from homeassistant.config import load_yaml_config_file
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
from homeassistant.util.yaml import dump
from .const import (
    KEY_BANS_ENABLED, KEY_BANNED_IPS, KEY_LOGIN_THRESHOLD,
    KEY_FAILED_LOGIN_ATTEMPTS)
from .util import get_real_ip

_LOGGER = logging.getLogger(__name__)

NOTIFICATION_ID_BAN = 'ip-ban'
NOTIFICATION_ID_LOGIN = 'http-login'

IP_BANS_FILE = 'ip_bans.yaml'
ATTR_BANNED_AT = "banned_at"

SCHEMA_IP_BAN_ENTRY = vol.Schema({
    vol.Optional('banned_at'): vol.Any(None, cv.datetime)
})


@middleware
@asyncio.coroutine
def ban_middleware(__tmp5, __tmp3):
    """IP Ban middleware."""
    if not __tmp5.app[KEY_BANS_ENABLED]:
        return (yield from __tmp3(__tmp5))

    if KEY_BANNED_IPS not in __tmp5.app:
        hass = __tmp5.app['hass']
        __tmp5.app[KEY_BANNED_IPS] = yield from hass.async_add_job(
            load_ip_bans_config, hass.config.path(IP_BANS_FILE))

    # Verify if IP is not banned
    ip_address_ = get_real_ip(__tmp5)

    is_banned = any(__tmp4.ip_address == ip_address_
                    for __tmp4 in __tmp5.app[KEY_BANNED_IPS])

    if is_banned:
        raise HTTPForbidden()

    try:
        return (yield from __tmp3(__tmp5))
    except HTTPUnauthorized:
        yield from __tmp1(__tmp5)
        raise


@asyncio.coroutine
def __tmp1(__tmp5):
    """Process a wrong login attempt."""
    remote_addr = get_real_ip(__tmp5)

    msg = ('Login attempt or request with invalid authentication '
           'from {}'.format(remote_addr))
    _LOGGER.warning(msg)
    persistent_notification.async_create(
        __tmp5.app['hass'], msg, 'Login attempt failed',
        NOTIFICATION_ID_LOGIN)

    if (not __tmp5.app[KEY_BANS_ENABLED] or
            __tmp5.app[KEY_LOGIN_THRESHOLD] < 1):
        return

    if KEY_FAILED_LOGIN_ATTEMPTS not in __tmp5.app:
        __tmp5.app[KEY_FAILED_LOGIN_ATTEMPTS] = defaultdict(int)

    __tmp5.app[KEY_FAILED_LOGIN_ATTEMPTS][remote_addr] += 1

    if (__tmp5.app[KEY_FAILED_LOGIN_ATTEMPTS][remote_addr] >
            __tmp5.app[KEY_LOGIN_THRESHOLD]):
        new_ban = IpBan(remote_addr)
        __tmp5.app[KEY_BANNED_IPS].append(new_ban)

        hass = __tmp5.app['hass']
        yield from hass.async_add_job(
            __tmp2, hass.config.path(IP_BANS_FILE), new_ban)

        _LOGGER.warning(
            "Banned IP %s for too many login attempts", remote_addr)

        persistent_notification.async_create(
            hass,
            'Too many login attempts from {}'.format(remote_addr),
            'Banning IP address', NOTIFICATION_ID_BAN)


class IpBan(object):
    """Represents banned IP address."""

    def __tmp6(__tmp0, __tmp4: <FILL>, banned_at: datetime=None) -> None:
        """Initialize IP Ban object."""
        __tmp0.ip_address = ip_address(__tmp4)
        __tmp0.banned_at = banned_at or datetime.utcnow()


def load_ip_bans_config(path):
    """Load list of banned IPs from config file."""
    ip_list = []

    if not os.path.isfile(path):
        return ip_list

    try:
        list_ = load_yaml_config_file(path)
    except HomeAssistantError as err:
        _LOGGER.error('Unable to load %s: %s', path, str(err))
        return ip_list

    for __tmp4, ip_info in list_.items():
        try:
            ip_info = SCHEMA_IP_BAN_ENTRY(ip_info)
            ip_list.append(IpBan(__tmp4, ip_info['banned_at']))
        except vol.Invalid as err:
            _LOGGER.error("Failed to load IP ban %s: %s", ip_info, err)
            continue

    return ip_list


def __tmp2(path, __tmp4):
    """Update config file with new banned IP address."""
    with open(path, 'a') as out:
        ip_ = {str(__tmp4.ip_address): {
            ATTR_BANNED_AT: __tmp4.banned_at.strftime("%Y-%m-%dT%H:%M:%S")
        }}
        out.write('\n')
        out.write(dump(ip_))
