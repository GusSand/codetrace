from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
__typ0 : TypeAlias = "str"
from Crypto.Hash import (
    SHA256 as _sha256,
    SHA512 as _sha512,
)
from Crypto.Protocol.KDF import (
    scrypt as _scrypt,
    HKDF as _HKDF,
    PBKDF2 as _PBKDF2,
)
from Crypto.Cipher import (
    AES as _AES
)


def SHA256(__tmp6):
    return _sha256.new(__tmp6).digest()


def scrypt(*, __tmp5, __tmp1, __tmp2, r: int, p, __tmp3) -> __typ1:
    assert(__tmp2 < 2**(128 * r / 8))
    res = _scrypt(__tmp5=__tmp5, __tmp1=__tmp1, key_len=__tmp3, N=__tmp2, r=r, p=p)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp5, __tmp1, __tmp3, c, __tmp4) :
    assert('sha' in __tmp4)
    _hash = _sha256 if 'sha256' in __tmp4 else _sha512
    res = _PBKDF2(__tmp5=__tmp5, __tmp1=__tmp1, dkLen=__tmp3, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1, IKM: __typ1, L: <FILL>) :
    res = _HKDF(master=IKM, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, key, __tmp0):
    return _AES.new(key=key, mode=_AES.MODE_CTR, initial_value=__tmp0, nonce=b'')
