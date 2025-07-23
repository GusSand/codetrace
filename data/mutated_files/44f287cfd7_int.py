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


def SHA256(x):
    return _sha256.new(x).digest()


def scrypt(*, __tmp0: __typ0, __tmp1: __typ0, n, r: <FILL>, p: int, dklen: int) :
    assert(n < 2**(128 * r / 8))
    res = _scrypt(__tmp0=__tmp0, __tmp1=__tmp1, key_len=dklen, N=n, r=r, p=p)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp0, __tmp1: __typ1, dklen, c, prf) :
    assert('sha' in prf)
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(__tmp0=__tmp0, __tmp1=__tmp1, dkLen=dklen, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1: __typ1, __tmp2: __typ1, L: int) -> __typ1:
    res = _HKDF(master=__tmp2, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, key: __typ1, iv: __typ1):
    return _AES.new(key=key, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
