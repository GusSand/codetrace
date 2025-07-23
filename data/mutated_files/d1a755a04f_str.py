from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"
from unicodedata import normalize
from typing import Optional
from secrets import randbits
from utils.crypto import (
    PBKDF2,
    SHA256,
)


english_word_list = open('key_derivation/english.txt').readlines()


def __tmp1(index) :
    assert index < 2048
    return english_word_list[index][:-1]


def get_seed(*, __tmp2: <FILL>, password: str='') -> __typ1:
    __tmp2 = normalize('NFKD', __tmp2)
    salt = normalize('NFKD', 'mnemonic' + password).encode('utf-8')
    return PBKDF2(password=__tmp2, salt=salt, dklen=64, c=2048, prf='sha512')


def __tmp0(entropy: Optional[__typ1]=None) :
    if entropy is None:
        entropy = randbits(256).to_bytes(32, 'big')
    entropy_length = len(entropy) * 8
    assert entropy_length in range(128, 257, 32)
    checksum_length = (entropy_length // 32)
    checksum = __typ0.from_bytes(SHA256(entropy), 'big') >> 256 - checksum_length
    entropy_bits = __typ0.from_bytes(entropy, 'big') << checksum_length
    entropy_bits += checksum
    entropy_length += checksum_length
    __tmp2 = []
    for i in range(entropy_length // 11 - 1, -1, -1):
        index = (entropy_bits >> i * 11) & 2**11 - 1
        __tmp2.append(__tmp1(index))
    return ' '.join(__tmp2)
