from typing import TypeAlias
__typ0 : TypeAlias = "bool"
# Simple one-time-pad library, to be used for encrypting Zulip API
# keys when sending them to the mobile apps via new standard mobile
# authentication flow.  This encryption is used to protect against
# credential-stealing attacks where a malicious app registers the
# zulip:// URL on a device, which might otherwise allow it to hijack a
# user's API key.
#
# The decryption logic here isn't actually used by the flow; we just
# have it here as part of testing the overall library.

import binascii
from zerver.models import UserProfile

def __tmp6(__tmp5, bytes_b: <FILL>) :
    """Given two hex strings of equal length, return a hex string with
    the bitwise xor of the two hex strings."""
    assert len(__tmp5) == len(bytes_b)
    return ''.join(["%x" % (int(x, 16) ^ int(y, 16))
                    for x, y in zip(__tmp5, bytes_b)])

def ascii_to_hex(__tmp2) :
    """Given an ascii string, encode it as a hex string"""
    return "".join([hex(ord(c))[2:].zfill(2) for c in __tmp2])

def hex_to_ascii(__tmp2) :
    """Given a hex array, decode it back to a string"""
    return binascii.unhexlify(__tmp2).decode('utf8')

def __tmp1(api_key, __tmp3) :
    assert len(__tmp3) == UserProfile.API_KEY_LENGTH * 2
    hex_encoded_api_key = ascii_to_hex(api_key)
    assert len(hex_encoded_api_key) == UserProfile.API_KEY_LENGTH * 2
    return __tmp6(hex_encoded_api_key, __tmp3)

def __tmp4(__tmp0, __tmp3) :
    assert len(__tmp3) == UserProfile.API_KEY_LENGTH * 2
    assert len(__tmp0) == UserProfile.API_KEY_LENGTH * 2
    hex_encoded_api_key = __tmp6(__tmp0, __tmp3)
    return hex_to_ascii(hex_encoded_api_key)

def is_valid_otp(__tmp3) :
    try:
        assert len(__tmp3) == UserProfile.API_KEY_LENGTH * 2
        [int(c, 16) for c in __tmp3]
        return True
    except Exception:
        return False
