from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
from utils.crypto import (
    HKDF,
    SHA256,
)
from py_ecc.optimized_bls12_381 import curve_order as bls_curve_order
from typing import List


def flip_bits(input) :
    return input ^ (2**256 - 1)


def IKM_to_lamport_SK(*, __tmp1: __typ0, __tmp0) -> List[__typ0]:
    OKM = HKDF(__tmp0=__tmp0, __tmp1=__tmp1, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def parent_SK_to_lamport_PK(*, parent_SK: <FILL>, __tmp5: int) -> __typ0:
    __tmp0 = __tmp5.to_bytes(4, byteorder='big')
    __tmp1 = parent_SK.to_bytes(32, byteorder='big')
    lamport_0 = IKM_to_lamport_SK(__tmp1=__tmp1, __tmp0=__tmp0)
    not_IKM = flip_bits(parent_SK).to_bytes(32, byteorder='big')
    lamport_1 = IKM_to_lamport_SK(__tmp1=not_IKM, __tmp0=__tmp0)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, __tmp1: __typ0) -> int:
    okm = HKDF(__tmp0=b'BLS-SIG-KEYGEN-SALT-', __tmp1=__tmp1, L=48)
    return int.from_bytes(okm, byteorder='big') % bls_curve_order


def __tmp2(*, parent_SK: int, __tmp5: int) -> int:
    assert(__tmp5 >= 0 and __tmp5 < 2**32)
    lamport_PK = parent_SK_to_lamport_PK(parent_SK=parent_SK, __tmp5=__tmp5)
    return HKDF_mod_r(__tmp1=lamport_PK)


def __tmp3(__tmp4: __typ0) -> int:
    assert(len(__tmp4) >= 16)
    return HKDF_mod_r(__tmp1=__tmp4)
