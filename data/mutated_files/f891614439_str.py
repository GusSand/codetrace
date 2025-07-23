from typing import TypeAlias
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


def scrypt(*, password, __tmp1: <FILL>, n: __typ0, r, p: __typ0, dklen: __typ0) -> bytes:
    assert(n < 2**(128 * r / 8))
    res = _scrypt(password=password, __tmp1=__tmp1, key_len=dklen, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, password: str, __tmp1: bytes, dklen: __typ0, c: __typ0, prf) :
    assert('sha' in prf)
    _hash = _sha256 if 'sha256' in prf else _sha512
    res = _PBKDF2(password=password, __tmp1=__tmp1, dkLen=dklen, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1, IKM: bytes, L) :
    res = _HKDF(master=IKM, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, __tmp0: bytes, iv):
    return _AES.new(__tmp0=__tmp0, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
