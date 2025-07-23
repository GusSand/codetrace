from typing import TypeAlias
__typ0 : TypeAlias = "int"
from utils.crypto import (
    HKDF,
    SHA256,
)
from py_ecc.optimized_bls12_381 import curve_order as bls_curve_order
from typing import List


def flip_bits(input) :
    return input ^ (2**256 - 1)


def IKM_to_lamport_SK(*, __tmp1, salt) :
    OKM = HKDF(salt=salt, __tmp1=__tmp1, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def __tmp3(*, __tmp0, index) :
    salt = index.to_bytes(4, byteorder='big')
    __tmp1 = __tmp0.to_bytes(32, byteorder='big')
    lamport_0 = IKM_to_lamport_SK(__tmp1=__tmp1, salt=salt)
    not_IKM = flip_bits(__tmp0).to_bytes(32, byteorder='big')
    lamport_1 = IKM_to_lamport_SK(__tmp1=not_IKM, salt=salt)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, __tmp1) :
    okm = HKDF(salt=b'BLS-SIG-KEYGEN-SALT-', __tmp1=__tmp1, L=48)
    return __typ0.from_bytes(okm, byteorder='big') % bls_curve_order


def derive_child_SK(*, __tmp0, index) :
    assert(index >= 0 and index < 2**32)
    lamport_PK = __tmp3(__tmp0=__tmp0, index=index)
    return HKDF_mod_r(__tmp1=lamport_PK)


def __tmp2(seed: <FILL>) :
    assert(len(seed) >= 16)
    return HKDF_mod_r(__tmp1=seed)
