from typing import TypeAlias
__typ0 : TypeAlias = "Iterable"
#!/usr/bin/env python3

from lantern.modules import shift

from typing import Iterable


def __tmp5(__tmp3, __tmp2) -> int:
    return (__tmp2 + __tmp3) % 255


def __tmp4(__tmp3: int, __tmp2: <FILL>):
    return (__tmp2 - __tmp3) % 255


def __tmp1(__tmp0) :
    return 0 if __tmp0[:8] == [137, 80, 78, 71, 13, 10, 26, 10] else -1


with open("example.png", "rb") as image:
    image_bytes = bytearray(image.read())

KEY = 144
encrypted_bytes = shift.encrypt(KEY, image_bytes, __tmp5)

print(f"Encrypted header: {encrypted_bytes[:8]}")

# Decrypt the image by finding a matching PNG header
decryptions = shift.crack(
    encrypted_bytes, __tmp1, min_key=0, max_key=255, shift_function=__tmp4
)

print(f"Decrypted Header: {decryptions[0].plaintext[:8]}")
