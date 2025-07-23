from typing import TypeAlias
__typ0 : TypeAlias = "int"
from utils.crypto import (
    HKDF,
    SHA256,
)
from py_ecc.optimized_bls12_381 import curve_order as bls_curve_order
from typing import List


def __tmp2(input) :
    return input ^ (2**256 - 1)


def __tmp8(*, __tmp1: bytes, __tmp0: bytes) -> List[bytes]:
    OKM = HKDF(__tmp0=__tmp0, __tmp1=__tmp1, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def __tmp7(*, __tmp3: __typ0, __tmp9: __typ0) -> bytes:
    __tmp0 = __tmp9.to_bytes(4, byteorder='big')
    __tmp1 = __tmp3.to_bytes(32, byteorder='big')
    lamport_0 = __tmp8(__tmp1=__tmp1, __tmp0=__tmp0)
    not_IKM = __tmp2(__tmp3).to_bytes(32, byteorder='big')
    lamport_1 = __tmp8(__tmp1=not_IKM, __tmp0=__tmp0)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, __tmp1: <FILL>) -> __typ0:
    okm = HKDF(__tmp0=b'BLS-SIG-KEYGEN-SALT-', __tmp1=__tmp1, L=48)
    return __typ0.from_bytes(okm, byteorder='big') % bls_curve_order


def __tmp4(*, __tmp3: __typ0, __tmp9: __typ0) -> __typ0:
    assert(__tmp9 >= 0 and __tmp9 < 2**32)
    lamport_PK = __tmp7(__tmp3=__tmp3, __tmp9=__tmp9)
    return HKDF_mod_r(__tmp1=lamport_PK)


def __tmp5(__tmp6) -> __typ0:
    assert(len(__tmp6) >= 16)
    return HKDF_mod_r(__tmp1=__tmp6)
