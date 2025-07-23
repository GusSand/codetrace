#!/usr/bin/env python3

from lantern.modules import shift
import binascii


def __tmp0(key: <FILL>, byte) -> int:
    """Subtract byte by key"""
    return byte - key


ciphertext = [0xed, 0xbc, 0xcd, 0xfe]

KEY = 15
decryption = shift.decrypt(KEY, ciphertext, __tmp0)
print(binascii.hexlify(bytearray(decryption)))
