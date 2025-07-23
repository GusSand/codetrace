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


def SHA256(__tmp6):
    return _sha256.new(__tmp6).digest()


def scrypt(*, __tmp3, __tmp1: __typ1, __tmp2: __typ0, r, p, dklen: __typ0) :
    assert(__tmp2 < 2**(128 * r / 8))
    res = _scrypt(__tmp3=__tmp3, __tmp1=__tmp1, key_len=dklen, N=__tmp2, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp3, __tmp1, dklen: __typ0, c: __typ0, prf: __typ1) :
    assert('sha' in prf)
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(__tmp3=__tmp3, __tmp1=__tmp1, dkLen=dklen, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1: bytes, IKM: <FILL>, L) -> bytes:
    res = _HKDF(master=IKM, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def __tmp4(*, __tmp5, __tmp0):
    return _AES.new(__tmp5=__tmp5, mode=_AES.MODE_CTR, initial_value=__tmp0, nonce=b'')
