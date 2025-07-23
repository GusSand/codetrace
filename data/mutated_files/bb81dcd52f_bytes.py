from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
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


def scrypt(*, __tmp0: __typ1, __tmp1: __typ1, n: __typ0, r: __typ0, p: __typ0, __tmp2: __typ0) -> bytes:
    assert(n < 2**(128 * r / 8))
    res = _scrypt(__tmp0=__tmp0, __tmp1=__tmp1, key_len=__tmp2, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp0: __typ1, __tmp1: <FILL>, __tmp2: __typ0, c: __typ0, prf: __typ1) -> bytes:
    assert('sha' in prf)
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(__tmp0=__tmp0, __tmp1=__tmp1, dkLen=__tmp2, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1, __tmp3: bytes, L: __typ0) -> bytes:
    res = _HKDF(master=__tmp3, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, key: bytes, iv: bytes):
    return _AES.new(key=key, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
