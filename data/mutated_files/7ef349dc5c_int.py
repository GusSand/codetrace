from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
__typ0 : TypeAlias = "str"
from unicodedata import normalize
from typing import Optional
from secrets import randbits
from utils.crypto import (
    PBKDF2,
    SHA256,
)


english_word_list = open('key_derivation/english.txt').readlines()


def __tmp1(__tmp4: <FILL>) :
    assert __tmp4 < 2048
    return english_word_list[__tmp4][:-1]


def __tmp2(*, __tmp3, password: __typ0='') :
    __tmp3 = normalize('NFKD', __tmp3)
    salt = normalize('NFKD', 'mnemonic' + password).encode('utf-8')
    return PBKDF2(password=__tmp3, salt=salt, dklen=64, c=2048, prf='sha512')


def __tmp0(entropy: Optional[__typ1]=None) -> __typ0:
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    assert entropy_length in range(128, 257, 32)
    checksum_length = (entropy_length // 32)
    checksum = int.from_bytes(SHA256(entropy), 'big') >> 256 - checksum_length
    entropy_bits = int.from_bytes(entropy, 'big') << checksum_length
    entropy_bits += checksum
    entropy_length += checksum_length
    __tmp3 = []
    for i in range(entropy_length // 11 - 1, -1, -1):
        __tmp4 = (entropy_bits >> i * 11) & 2**11 - 1
        __tmp3.append(__tmp1(__tmp4))
    return ' '.join(__tmp3)
