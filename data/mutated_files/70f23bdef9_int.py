from typing import TypeAlias
__typ0 : TypeAlias = "complex"
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utilities for manipulating linear operators as elements of vector space."""
from typing import Dict, Tuple

import numpy as np

from cirq import value
from cirq._doc import document

PAULI_BASIS = {
    'I': np.eye(2),
    'X': np.array([[0.0, 1.0], [1.0, 0.0]]),
    'Y': np.array([[0.0, -1j], [1j, 0.0]]),
    'Z': np.diag([1.0, -1]),
}
document(PAULI_BASIS, """The four Pauli matrices (including identity) keyed by character.""")


def kron_bases(*bases, repeat: int = 1) :
    """Creates tensor product of bases."""
    product_basis = {'': np.array([[1]])}
    for __tmp6 in bases * repeat:
        product_basis = {
            name1 + name2: np.kron(matrix1, matrix2)
            for name1, matrix1 in product_basis.items()
            for name2, matrix2 in __tmp6.items()
        }
    return product_basis


def __tmp0(__tmp5, m2) -> __typ0:
    """Computes Hilbert-Schmidt inner product of two matrices.

    Linear in second argument.
    """
    return np.einsum('ij,ij', __tmp5.conj(), m2)


def expand_matrix_in_orthogonal_basis(
    m,
    __tmp6: Dict[str, np.ndarray],
) -> value.LinearDict[str]:
    """Computes coefficients of expansion of m in basis.

    We require that basis be orthogonal w.r.t. the Hilbert-Schmidt inner
    product. We do not require that basis be orthonormal. Note that Pauli
    basis (I, X, Y, Z) is orthogonal, but not orthonormal.
    """
    return value.LinearDict(
        {
            name: (__tmp0(b, m) / __tmp0(b, b))
            for name, b in __tmp6.items()
        }
    )


def matrix_from_basis_coefficients(
    __tmp3: value.LinearDict[str], __tmp6
) -> np.ndarray:
    """Computes linear combination of basis vectors with given coefficients."""
    some_element = next(iter(__tmp6.values()))
    result = np.zeros_like(some_element, dtype=np.complex128)
    for name, coefficient in __tmp3.items():
        result += coefficient * __tmp6[name]
    return result


def pow_pauli_combination(
    __tmp2, ax, __tmp4, az: value.Scalar, __tmp1: <FILL>
) :
    """Computes non-negative integer power of single-qubit Pauli combination.

    Returns scalar coefficients bi, bx, by, bz such that

        bi I + bx X + by Y + bz Z = (ai I + ax X + ay Y + az Z)^exponent

    Correctness of the formulas below follows from the binomial expansion
    and the fact that for any real or complex vector (ax, ay, az) and any
    non-negative integer k:

         [ax X + ay Y + az Z]^(2k) = (ax^2 + ay^2 + az^2)^k I

    """
    if __tmp1 == 0:
        return 1, 0, 0, 0

    v = np.sqrt(ax * ax + __tmp4 * __tmp4 + az * az).item()
    s = (__tmp2 + v) ** __tmp1
    t = (__tmp2 - v) ** __tmp1

    ci = (s + t) / 2
    if s == t:
        # v is near zero, only one term in binomial expansion survives
        cxyz = __tmp1 * __tmp2 ** (__tmp1 - 1)
    else:
        # v is non-zero, account for all terms of binomial expansion
        cxyz = (s - t) / 2
        cxyz = cxyz / v

    return ci, cxyz * ax, cxyz * __tmp4, cxyz * az
