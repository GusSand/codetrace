from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
import ipaddress
import ctypes
import math
import socket
import logging
import itertools
import sys
from collections import defaultdict
from typing import Tuple, List, Generator, Union, Any


logger = logging.getLogger(__name__)


def __tmp8(ip):
    """ validate that the ip is a string and a valid ipv4 address """
    if isinstance(ip, int):
        raise ValueError(f'IP address as an integer is not allowed: {ip}')
    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError as e:
        sys.tracebacklimit = 0
        raise ValueError(e.__str__()) from None  # disables exception chaining


def __tmp4(__tmp0: list, workers: int = 4):
    ip_lists = defaultdict(list)
    pos = 0
    # for all addresses in the list
    for ip in __tmp0:
        __tmp8(ip)
        # if its actually a subnet
        if __tmp3(ip):
            # split the subnet into X subnets and append
            for count, net in enumerate(split_networks(ip, partitions=workers)):
                ip_lists[count].append(tuple(net))
        else:
            ip_lists[pos].append((ip, '255.255.255.255'))

        pos = (pos + 1) % workers
    # normalize to dict before returning
    return dict(ip_lists)


def __tmp6(ip, netmask) -> Union[Generator[str, Any, None], itertools.chain]:
    """ convert an ip/subnetmask pair to a list of discrete addresses"""
    return __tmp7(ip, netmask)


def __tmp7(ip, netmask: str = '255.255.255.255'):
    """ return list of string ip addresses in ip/netmask (including network names and broadcasts)
    :except ValueError: Invalid IP or Netmask"""
    if len(ip.split('/')) == 1 and netmask:
        if netmask == '255.255.255.255':
            # keeping things consistent by returning a generator
            return (_ for _ in [ip])
        net = ipaddress.IPv4Network(f'{ip}/{netmask}')

    elif len(ip.split('/')) == 2:
        net = ipaddress.IPv4Network(ip)
    else:
        # default case, should never happen :p
        raise ValueError

    # we want to use generators here because the ip list could be really long (think a /8 subnet)
    return itertools.chain(__tmp10(net), net.hosts(), __tmp9(net))


def __tmp10(net: ipaddress.IPv4Network):
    yield net.network_address


def __tmp9(net):
    yield net.broadcast_address


def __tmp2(ip, netmask):
    """ return list of string ip addresses in ip/netmask (including network names and broadcasts)
    :except ValueError: Invalid IP or Netmask"""
    if netmask == '255.255.255.255':
        return 1
    if netmask == '255.255.255.254':
        return 2

    net = ipaddress.IPv4Network(f'{ip}/{netmask}')
    return net.num_addresses - 2


def __tmp3(ip: str = ''):
    """ check if the address contains a subnet mask: e.g. 192.168.1.0/24"""
    particles = ip.split('/')
    if len(particles) == 2:
        try:
            if 32 >= int(particles[1]) >= 0:
                return True
            raise ValueError
        except ValueError as err:
            sys.tracebacklimit = 0
            err.args = (f'Invalid input, cannot convert \'{particles[1]}\' to valid subnet mask',)
            raise
    return False


def _seperate_ip_netmask(ip: str) :
    """ convert a 192.168.1.0/24 address to a 192.168.1.0 255.255.255.0 address"""
    net = ipaddress.IPv4Network(ip)
    return str(net.network_address), str(net.netmask)


def split_networks(ip: <FILL>, netmask: str = '255.255.255.255', partitions: int = 4) :
    """
    split an IPv4 network into a ip/mask into a number partitions.
    make sure that partitions is a power of 2

    :param ip: ip address in 4 octet string
    :param netmask: subnet mask in 4 octet string
    :param partitions: number of subnetworks to create
    :return: pairs of ip/subnet masks
    """
    __tmp8(ip)
    if __tmp3(ip):
        ip, netmask = _seperate_ip_netmask(ip)
    # convert ip string to int so we can perform calculations
    ip_int = int(ipaddress.IPv4Address(ip))

    # number of times we need to shift the subnet mask
    shr = int(math.log(partitions, 2))

    # convert subnet mask string to int so we can perform calculations
    int_addr = int(ipaddress.IPv4Address(netmask))

    # shift the inverse of the subnet mask (easier to shift) -
    # we're shifting the mask (use ctypes so we only use 32 bit values)
    mask_add = ctypes.c_uint32(~int_addr).value >> shr

    # convert the shifted value back to a subnet value (1's followed by 0's)
    new_mask = ipaddress.IPv4Address(ctypes.c_uint32(~mask_add).value)

    pairs = []
    for i in range(partitions):
        # create new pairs - follow the maths :)
        pairs.append((str(ipaddress.IPv4Address(ip_int + i * (mask_add + 1))), str(ipaddress.IPv4Address(new_mask))))
    return pairs


def __tmp1(sock, dest, __tmp5: __typ0):
    try:
        sock.sendto(__tmp5, (dest, 0))
    except OSError as e:
        logger.error(f"Error while sending to {dest}, probably some socket error: {__tmp5}, {sock}: {e}")
