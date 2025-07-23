from typing import TypeAlias
__typ0 : TypeAlias = "int"
#!/usr/bin/env python3

from lantern.modules import shift

from typing import Iterable


def __tmp3(key: __typ0, __tmp1: __typ0) :
    return (__tmp1 + key) % 255


def __tmp2(key: __typ0, __tmp1: __typ0):
    return (__tmp1 - key) % 255


def header_matcher(__tmp0: <FILL>) :
    return 0 if __tmp0[:8] == [137, 80, 78, 71, 13, 10, 26, 10] else -1


with open("example.png", "rb") as image:
    image_bytes = bytearray(image.read())

KEY = 144
encrypted_bytes = shift.encrypt(KEY, image_bytes, __tmp3)

print(f"Encrypted header: {encrypted_bytes[:8]}")

# Decrypt the image by finding a matching PNG header
decryptions = shift.crack(
    encrypted_bytes, header_matcher, min_key=0, max_key=255, shift_function=__tmp2
)

print(f"Decrypted Header: {decryptions[0].plaintext[:8]}")
