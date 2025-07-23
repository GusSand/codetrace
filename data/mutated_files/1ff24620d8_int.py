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


def SHA256(__tmp9):
    return _sha256.new(__tmp9).digest()


def scrypt(*, __tmp6, __tmp1, __tmp3, r, p, __tmp4) :
    assert(__tmp3 < 2**(128 * r / 8))
    res = _scrypt(__tmp6=__tmp6, __tmp1=__tmp1, key_len=__tmp4, N=__tmp3, r=r, p=p)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp6, __tmp1, __tmp4, c: <FILL>, __tmp5) :
    assert('sha' in __tmp5)
    _hash = _sha256 if 'sha256' in __tmp5 else _sha512
    res = _PBKDF2(__tmp6=__tmp6, __tmp1=__tmp1, dkLen=__tmp4, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1, __tmp2, L) :
    res = _HKDF(master=__tmp2, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def __tmp7(*, __tmp8, __tmp0: __typ1):
    return _AES.new(__tmp8=__tmp8, mode=_AES.MODE_CTR, initial_value=__tmp0, nonce=b'')
