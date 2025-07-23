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


def SHA256(__tmp4):
    return _sha256.new(__tmp4).digest()


def scrypt(*, __tmp3, __tmp0, n: int, r, p, __tmp1: <FILL>) -> __typ1:
    assert(n < 2**(128 * r / 8))
    res = _scrypt(__tmp3=__tmp3, __tmp0=__tmp0, key_len=__tmp1, N=n, r=r, p=p)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp3, __tmp0, __tmp1, c, prf) :
    assert('sha' in prf)
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(__tmp3=__tmp3, __tmp0=__tmp0, dkLen=__tmp1, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp0, IKM, __tmp2) :
    res = _HKDF(master=IKM, key_len=__tmp2, __tmp0=__tmp0, hashmod=_sha256)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, key, iv):
    return _AES.new(key=key, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
