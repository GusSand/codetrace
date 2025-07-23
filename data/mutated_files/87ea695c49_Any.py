from typing import TypeAlias
__typ1 : TypeAlias = "bool"
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

from typing import (
    Any,
    TypeVar,
    Optional,
)

import numpy as np
from typing_extensions import Protocol

from cirq import qis
from cirq._doc import doc_private
from cirq.protocols import qid_shape_protocol
from cirq.protocols.apply_unitary_protocol import ApplyUnitaryArgs
from cirq.protocols.decompose_protocol import (
    _try_decompose_into_operations_and_qubits,
)

TDefault = TypeVar('TDefault')


class __typ0(Protocol):
    """An object that explicitly specifies whether it has a unitary effect."""

    @doc_private
    def _has_unitary_(__tmp2) -> __typ1:
        """Determines whether the receiver has a unitary effect.

        This method is used preferentially by the global `cirq.has_unitary`
        method, because this method is much cheaper than the fallback strategies
        such as checking `value._unitary_` (which causes a large matrix to be
        computed).

        Returns:
            Whether or not the receiving object (`self`) has a unitary effect.
        """


def __tmp3(__tmp0, *, allow_decompose: __typ1 = True) :
    """Determines whether the value has a unitary effect.

    Determines whether `val` has a unitary effect by attempting the following
    strategies:

    1. Try to use `val.has_unitary()`.
        Case a) Method not present or returns `NotImplemented`.
            Inconclusive.
        Case b) Method returns `True`.
            Unitary.
        Case c) Method returns `False`.
            Not unitary.

    2. Try to use `val._decompose_()`.
        Case a) Method not present or returns `NotImplemented` or `None`.
            Inconclusive.
        Case b) Method returns an OP_TREE containing only unitary operations.
            Unitary.
        Case c) Method returns an OP_TREE containing non-unitary operations.
            Not Unitary.

    3. Try to use `val._apply_unitary_(args)`.
        Case a) Method not present or returns `NotImplemented`.
            Inconclusive.
        Case b) Method returns a numpy array.
            Unitary.
        Case c) Method returns `None`.
            Not unitary.

    4. Try to use `val._unitary_()`.
        Case a) Method not present or returns `NotImplemented`.
            Continue to next strategy.
        Case b) Method returns a numpy array.
            Unitary.
        Case c) Method returns `None`.
            Not unitary.

    It is assumed that, when multiple of these strategies give a conclusive
    result, that these results will all be consistent with each other. If all
    strategies are inconclusive, the value is classified as non-unitary.

    Args:
        The value that may or may not have a unitary effect.

    Returns:
        Whether or not `val` has a unitary effect.
    """
    strats = [
        __tmp5,
        __tmp6,
        __tmp4,
        __tmp1,
    ]
    if not allow_decompose:
        strats.remove(__tmp6)
    for strat in strats:
        result = strat(__tmp0)
        if result is not None:
            return result

    # If you can't tell that it's unitary, it's not unitary.
    return False


def __tmp5(__tmp0: Any) -> Optional[__typ1]:
    """Attempts to infer a value's unitary-ness via its _has_unitary_ method."""
    if hasattr(__tmp0, '_has_unitary_'):
        result = __tmp0._has_unitary_()
        if result is NotImplemented:
            return None
        return result
    return None


def __tmp1(__tmp0: <FILL>) :
    """Attempts to infer a value's unitary-ness via its _unitary_ method."""
    getter = getattr(__tmp0, '_unitary_', None)
    if getter is None:
        return None
    result = getter()
    return result is not NotImplemented and result is not None


def __tmp6(__tmp0: Any) :
    """Attempts to infer a value's unitary-ness via its _decompose_ method."""
    operations, _, _ = _try_decompose_into_operations_and_qubits(__tmp0)
    if operations is None:
        return None
    return all(__tmp3(op) for op in operations)


def __tmp4(__tmp0) -> Optional[__typ1]:
    """Attempts to infer a value's unitary-ness via its _apply_unitary_ method."""
    method = getattr(__tmp0, '_apply_unitary_', None)
    if method is None:
        return None

    val_qid_shape = qid_shape_protocol.qid_shape(__tmp0, None)
    if val_qid_shape is None:
        return None
    state = qis.one_hot(shape=val_qid_shape, dtype=np.complex64)
    buffer = np.empty_like(state)
    result = method(ApplyUnitaryArgs(state, buffer, range(len(val_qid_shape))))
    if result is NotImplemented:
        return None
    return result is not None
