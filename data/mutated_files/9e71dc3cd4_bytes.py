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


def scrypt(*, __tmp4: __typ1, __tmp0, n: __typ0, r, p, __tmp2) :
    assert(n < 2**(128 * r / 8))
    res = _scrypt(__tmp4=__tmp4, __tmp0=__tmp0, key_len=__tmp2, N=n, r=r, p=p)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp4, __tmp0, __tmp2, c, __tmp3) :
    assert('sha' in __tmp3)
    _hash = _sha256 if 'sha256' in __tmp3 else _sha512
    res = _PBKDF2(__tmp4=__tmp4, __tmp0=__tmp0, dkLen=__tmp2, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp0: <FILL>, __tmp1, L) :
    res = _HKDF(master=__tmp1, key_len=L, __tmp0=__tmp0, hashmod=_sha256)
    return res if isinstance(res, bytes) else res[0]  # PyCryptodome can return Tuple[bytes]


def AES_128_CTR(*, __tmp5, iv):
    return _AES.new(__tmp5=__tmp5, mode=_AES.MODE_CTR, initial_value=iv, nonce=b'')
