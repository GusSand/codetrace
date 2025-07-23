from typing import TypeAlias
__typ2 : TypeAlias = "memoryview"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "bool"
import struct
import collections
# pylint: disable=no-name-in-module
from pingscan.c_icmp import build as cbuild

__typ3 = collections.namedtuple('ICMPHeader', 'type code checksum')

ICMP_ECHO_REPLY = 0
ICMP_OFFSET_V4 = 20
MSG_ID_OFFSET_V4 = 24
SRC_IP_OFFSET_v4 = 12
ICMP_NETWORK_UNREACH = 3
MAX_SEQUENCE = 65535
IPv4 = 0
IPv6 = 1

msg_id_offset = MSG_ID_OFFSET_V4
offset = ICMP_OFFSET_V4
offset_src_ip = SRC_IP_OFFSET_v4


def parse(__tmp1: <FILL>) -> __typ3:
    icmp_header = __tmp1[ICMP_OFFSET_V4: ICMP_OFFSET_V4 + 8]
    icmp_type, code, checksum, _, _ = struct.unpack('bbHHh', icmp_header)
    return __typ3(icmp_type, code, checksum)


def build(seq=1, msg_id=1) -> bytes:
    __tmp1 = cbuild(seq, msg_id)
    return bytes(__tmp1)


def msg_id_match(__tmp1: __typ2, msg_id=1, pos: __typ0 = 0, family: __typ0 = IPv4) -> __typ0:
    return __typ0().from_bytes(__tmp1[msg_id_offset + pos:msg_id_offset + 2 + pos], byteorder='little') == msg_id


def __tmp0(__tmp1: __typ2, pos: __typ0 = 0, family: __typ0 = IPv4) -> __typ0:
    resp_ip = __typ0().from_bytes(__tmp1[offset_src_ip + pos:offset_src_ip + 4 + pos], byteorder='big')
    return resp_ip


def is_icmp_reply(__tmp1: __typ2, pos: __typ0 = 0, family: __typ0 = IPv4) :
    return __tmp1[offset + pos] == ICMP_ECHO_REPLY
