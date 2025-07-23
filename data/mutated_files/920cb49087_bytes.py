from typing import TypeAlias
__typ0 : TypeAlias = "int"
from utils.crypto import (
    HKDF,
    SHA256,
)
from py_ecc.optimized_bls12_381 import curve_order as bls_curve_order
from typing import List


def __tmp1(input) :
    return input ^ (2**256 - 1)


def __tmp6(*, __tmp0: <FILL>, salt: bytes) -> List[bytes]:
    OKM = HKDF(salt=salt, __tmp0=__tmp0, L=8160)
    lamport_SK = [OKM[i: i + 32] for i in range(0, 8160, 32)]
    return lamport_SK


def __tmp5(*, __tmp2: __typ0, index: __typ0) :
    salt = index.to_bytes(4, byteorder='big')
    __tmp0 = __tmp2.to_bytes(32, byteorder='big')
    lamport_0 = __tmp6(__tmp0=__tmp0, salt=salt)
    not_IKM = __tmp1(__tmp2).to_bytes(32, byteorder='big')
    lamport_1 = __tmp6(__tmp0=not_IKM, salt=salt)
    lamport_SKs = lamport_0 + lamport_1
    lamport_PKs = [SHA256(sk) for sk in lamport_SKs]
    compressed_PK = SHA256(b''.join(lamport_PKs))
    return compressed_PK


def HKDF_mod_r(*, __tmp0) -> __typ0:
    okm = HKDF(salt=b'BLS-SIG-KEYGEN-SALT-', __tmp0=__tmp0, L=48)
    return __typ0.from_bytes(okm, byteorder='big') % bls_curve_order


def __tmp3(*, __tmp2: __typ0, index: __typ0) :
    assert(index >= 0 and index < 2**32)
    lamport_PK = __tmp5(__tmp2=__tmp2, index=index)
    return HKDF_mod_r(__tmp0=lamport_PK)


def __tmp4(seed: bytes) :
    assert(len(seed) >= 16)
    return HKDF_mod_r(__tmp0=seed)
