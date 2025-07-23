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


def SHA256(__tmp9):
    return _sha256.new(__tmp9).digest()


def scrypt(*, __tmp6: __typ1, __tmp1: __typ1, n: __typ0, r: __typ0, p: __typ0, __tmp3: __typ0) -> bytes:
    assert(n < 2**(128 * r / 8))
    res = _scrypt(__tmp6=__tmp6, __tmp1=__tmp1, key_len=__tmp3, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp6: __typ1, __tmp1: bytes, __tmp3: __typ0, c: __typ0, __tmp4) -> bytes:
    assert('sha' in __tmp4)
    _hash = _sha256 if 'sha256' in __tmp4 else _sha512
    res = _PBKDF2(__tmp6=__tmp6, __tmp1=__tmp1, dkLen=__tmp3, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1, __tmp2: bytes, __tmp5) -> bytes:
    res = _HKDF(master=__tmp2, key_len=__tmp5, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def __tmp7(*, __tmp8: <FILL>, __tmp0: bytes):
    return _AES.new(__tmp8=__tmp8, mode=_AES.MODE_CTR, initial_value=__tmp0, nonce=b'')
