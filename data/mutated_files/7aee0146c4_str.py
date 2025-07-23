from typing import TypeAlias
__typ0 : TypeAlias = "Device"
__typ1 : TypeAlias = "HomeAssistantType"
"""Hass representation of an UPnP/IGD."""
import asyncio
from ipaddress import IPv4Address

import aiohttp

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import HomeAssistantType

from .const import LOGGER as _LOGGER


class __typ0:
    """Hass representation of an UPnP/IGD."""

    def __init__(__tmp1, igd_device):
        """Initializer."""
        __tmp1._igd_device = igd_device
        __tmp1._mapped_ports = []

    @classmethod
    async def async_discover(cls, __tmp0):
        """Discovery UPNP/IGD devices."""
        _LOGGER.debug('Discovering UPnP/IGD devices')

        # discover devices
        from async_upnp_client.igd import IgdDevice
        discovery_infos = await IgdDevice.async_discover()

        # add extra info and store devices
        devices = []
        for discovery_info in discovery_infos:
            discovery_info['udn'] = discovery_info['usn'].split('::')[0]
            discovery_info['ssdp_description'] = discovery_info['location']
            discovery_info['source'] = 'async_upnp_client'
            _LOGGER.debug('Discovered device: %s', discovery_info)

            devices.append(discovery_info)

        return devices

    @classmethod
    async def async_create_device(cls,
                                  __tmp0,
                                  ssdp_description: <FILL>):
        """Create UPnP/IGD device."""
        # build async_upnp_client requester
        from async_upnp_client.aiohttp import AiohttpSessionRequester
        session = async_get_clientsession(__tmp0)
        requester = AiohttpSessionRequester(session, True)

        # create async_upnp_client device
        from async_upnp_client import UpnpFactory
        factory = UpnpFactory(requester,
                              disable_state_variable_validation=True)
        upnp_device = await factory.async_create_device(ssdp_description)

        # wrap with async_upnp_client.IgdDevice
        from async_upnp_client.igd import IgdDevice
        igd_device = IgdDevice(upnp_device, None)

        return cls(igd_device)

    @property
    def udn(__tmp1):
        """Get the UDN."""
        return __tmp1._igd_device.udn

    @property
    def name(__tmp1):
        """Get the name."""
        return __tmp1._igd_device.name

    @property
    def manufacturer(__tmp1):
        """Get the manufacturer."""
        return __tmp1._igd_device.manufacturer

    async def async_add_port_mappings(__tmp1, ports, __tmp2):
        """Add port mappings."""
        if __tmp2 == '127.0.0.1':
            _LOGGER.error(
                'Could not create port mapping, our IP is 127.0.0.1')

        # determine local ip, ensure sane IP
        __tmp2 = IPv4Address(__tmp2)

        # create port mappings
        for external_port, internal_port in ports.items():
            await __tmp1._async_add_port_mapping(external_port,
                                               __tmp2,
                                               internal_port)
            __tmp1._mapped_ports.append(external_port)

    async def _async_add_port_mapping(__tmp1,
                                      external_port,
                                      __tmp2,
                                      internal_port):
        """Add a port mapping."""
        # create port mapping
        from async_upnp_client import UpnpError
        _LOGGER.info('Creating port mapping %s:%s:%s (TCP)',
                     external_port, __tmp2, internal_port)
        try:
            await __tmp1._igd_device.async_add_port_mapping(
                remote_host=None,
                external_port=external_port,
                protocol='TCP',
                internal_port=internal_port,
                internal_client=__tmp2,
                enabled=True,
                description="Home Assistant",
                lease_duration=None)

            __tmp1._mapped_ports.append(external_port)
        except (asyncio.TimeoutError, aiohttp.ClientError, UpnpError):
            _LOGGER.error('Could not add port mapping: %s:%s:%s',
                          external_port, __tmp2, internal_port)

    async def async_delete_port_mappings(__tmp1):
        """Remove a port mapping."""
        for port in __tmp1._mapped_ports:
            await __tmp1._async_delete_port_mapping(port)

    async def _async_delete_port_mapping(__tmp1, external_port):
        """Remove a port mapping."""
        from async_upnp_client import UpnpError
        _LOGGER.info('Deleting port mapping %s (TCP)', external_port)
        try:
            await __tmp1._igd_device.async_delete_port_mapping(
                remote_host=None,
                external_port=external_port,
                protocol='TCP')

            __tmp1._mapped_ports.remove(external_port)
        except (asyncio.TimeoutError, aiohttp.ClientError, UpnpError):
            _LOGGER.error('Could not delete port mapping')

    async def async_get_total_bytes_received(__tmp1):
        """Get total bytes received."""
        return await __tmp1._igd_device.async_get_total_bytes_received()

    async def async_get_total_bytes_sent(__tmp1):
        """Get total bytes sent."""
        return await __tmp1._igd_device.async_get_total_bytes_sent()

    async def async_get_total_packets_received(__tmp1):
        """Get total packets received."""
        # pylint: disable=invalid-name
        return await __tmp1._igd_device.async_get_total_packets_received()

    async def async_get_total_packets_sent(__tmp1):
        """Get total packets sent."""
        return await __tmp1._igd_device.async_get_total_packets_sent()
