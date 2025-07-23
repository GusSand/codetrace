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

def __tmp8(__tmp7, __tmp4) :
    """Given two hex strings of equal length, return a hex string with
    the bitwise xor of the two hex strings."""
    assert len(__tmp7) == len(__tmp4)
    return ''.join(["%x" % (int(x, 16) ^ int(y, 16))
                    for x, y in zip(__tmp7, __tmp4)])

def __tmp5(__tmp1) :
    """Given an ascii string, encode it as a hex string"""
    return "".join([hex(ord(c))[2:].zfill(2) for c in __tmp1])

def __tmp2(__tmp1) :
    """Given a hex array, decode it back to a string"""
    return binascii.unhexlify(__tmp1).decode('utf8')

def otp_encrypt_api_key(__tmp3: <FILL>, otp) :
    assert len(otp) == UserProfile.API_KEY_LENGTH * 2
    hex_encoded_api_key = __tmp5(__tmp3)
    assert len(hex_encoded_api_key) == UserProfile.API_KEY_LENGTH * 2
    return __tmp8(hex_encoded_api_key, otp)

def __tmp6(__tmp0: str, otp: str) -> str:
    assert len(otp) == UserProfile.API_KEY_LENGTH * 2
    assert len(__tmp0) == UserProfile.API_KEY_LENGTH * 2
    hex_encoded_api_key = __tmp8(__tmp0, otp)
    return __tmp2(hex_encoded_api_key)

def __tmp9(otp) :
    try:
        assert len(otp) == UserProfile.API_KEY_LENGTH * 2
        [int(c, 16) for c in otp]
        return True
    except Exception:
        return False
