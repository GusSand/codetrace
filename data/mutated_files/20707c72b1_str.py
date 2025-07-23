from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
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


def SHA256(__tmp7):
    return _sha256.new(__tmp7).digest()


def scrypt(*, __tmp4: str, __tmp1: str, n, r: __typ0, p: __typ0, __tmp2: __typ0) -> __typ1:
    assert(n < 2**(128 * r / 8))
    res = _scrypt(__tmp4=__tmp4, __tmp1=__tmp1, key_len=__tmp2, N=n, r=r, p=p)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def PBKDF2(*, __tmp4, __tmp1: __typ1, __tmp2: __typ0, c, __tmp3: <FILL>) :
    assert('sha' in __tmp3)
    _hash = _sha256 if 'sha256' in __tmp3 else _sha512
    res = _PBKDF2(__tmp4=__tmp4, __tmp1=__tmp1, dkLen=__tmp2, count=c, hmac_hash_module=_hash)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def HKDF(*, __tmp1: __typ1, IKM, L) -> __typ1:
    res = _HKDF(master=IKM, key_len=L, __tmp1=__tmp1, hashmod=_sha256)
    return res if isinstance(res, __typ1) else res[0]  # PyCryptodome can return Tuple[bytes]


def __tmp5(*, __tmp6: __typ1, __tmp0: __typ1):
    return _AES.new(__tmp6=__tmp6, mode=_AES.MODE_CTR, initial_value=__tmp0, nonce=b'')
