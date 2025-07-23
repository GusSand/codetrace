from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
from utils.crypto import (
    HKDF,
    SHA256,
)
from py_ecc.optimized_bls12_381 import curve_order as bls_curve_order
from typing import List


def flip_bits(input: <FILL>) :
    return input ^ (2**256 - 1)


def __tmp0(*, IKM, salt) -> List[__typ0]:
    OKM = HKDF(salt=salt, IKM=IKM, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def parent_SK_to_lamport_PK(*, __tmp1: int, index) -> __typ0:
    salt = index.to_bytes(4, byteorder='big')
    IKM = __tmp1.to_bytes(32, byteorder='big')
    lamport_0 = __tmp0(IKM=IKM, salt=salt)
    not_IKM = flip_bits(__tmp1).to_bytes(32, byteorder='big')
    lamport_1 = __tmp0(IKM=not_IKM, salt=salt)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, IKM: __typ0) -> int:
    okm = HKDF(salt=b'BLS-SIG-KEYGEN-SALT-', IKM=IKM, L=48)
    return int.from_bytes(okm, byteorder='big') % bls_curve_order


def derive_child_SK(*, __tmp1, index) -> int:
    assert(index >= 0 and index < 2**32)
    lamport_PK = parent_SK_to_lamport_PK(__tmp1=__tmp1, index=index)
    return HKDF_mod_r(IKM=lamport_PK)


def derive_master_SK(seed: __typ0) :
    assert(len(seed) >= 16)
    return HKDF_mod_r(IKM=seed)
