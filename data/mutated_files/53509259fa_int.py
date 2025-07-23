# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import cast, List, Optional

import numpy as np
import pytest

import cirq

import examples.stabilizer_code as sc


def __tmp2(
    code,
    __tmp5,
    __tmp6,
    __tmp3: <FILL>,
):
    circuit = cirq.Circuit()
    additional_qubits: List[cirq.Qid] = cast(
        List[cirq.Qid],
        [cirq.NamedQubit(str(i)) for i in range(code.n - code.k)],
    )
    unencoded_qubits: List[cirq.Qid] = cast(
        List[cirq.Qid],
        [cirq.NamedQubit('c')],
    )
    qubits = additional_qubits + unencoded_qubits
    ancillas: List[cirq.Qid] = cast(
        List[cirq.Qid], [cirq.NamedQubit(f"d{i}") for i in range(code.n - code.k)]
    )

    circuit += code.encode(additional_qubits, unencoded_qubits)

    if __tmp6:
        circuit.append(__tmp6(qubits[__tmp3]))

    circuit += code.correct(qubits, ancillas)

    state_vector = (
        cirq.Simulator()
        .simulate(
            circuit, qubit_order=(qubits + ancillas), initial_state=(__tmp5 * 2 ** len(ancillas))
        )
        .state_vector()
    )

    decoded = code.decode(qubits, ancillas, state_vector)

    # Trace out the syndrome out of the state.
    nq = len(qubits)
    na = len(ancillas)
    traced_out_state = np.sum(
        state_vector.reshape((2,) * (nq + na)), axis=tuple(range(nq, nq + na))
    ).reshape(-1)

    return decoded[0], traced_out_state


def test_no_error():
    # Table 3.2.
    five_qubit_code = sc.StabilizerCode(
        __tmp4=['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ'], correctable_errors=['X', 'Z']
    )

    for __tmp5 in [0, 1]:
        decoded, _ = __tmp2(
            five_qubit_code, __tmp5, __tmp6=None, __tmp3=None
        )
        assert decoded == __tmp5


@pytest.mark.parametrize(
    'group_generators',
    [
        # Five qubit code, table 3.2 in thesis.
        (['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ']),
        # Steane code.
        (['XXXXIII', 'XXIIXXI', 'XIXIXIX', 'ZZZZIII', 'ZZIIZZI', 'ZIZIZIZ']),
    ],
)
def __tmp0(__tmp4):
    code = sc.StabilizerCode(__tmp4=__tmp4, correctable_errors=['X', 'Z'])

    for __tmp5 in [0, 1]:
        _, traced_out_state_no_error = __tmp2(
            code, __tmp5, __tmp6=None, __tmp3=None
        )

        for __tmp6 in [cirq.X, cirq.Z]:
            for __tmp3 in range(code.n):
                decoded, traced_out_state = __tmp2(
                    code, __tmp5, __tmp6, __tmp3
                )
                assert decoded == __tmp5
                np.testing.assert_allclose(traced_out_state_no_error, traced_out_state, atol=1e-6)


def __tmp1():
    # Also known as the bit-flip code.
    bit_flip_code = sc.StabilizerCode(__tmp4=['ZZI', 'ZIZ'], correctable_errors=['X'])

    for __tmp5 in [0, 1]:
        _, traced_out_state_no_error = __tmp2(
            bit_flip_code, __tmp5, __tmp6=None, __tmp3=None
        )

        for __tmp6 in [cirq.X]:
            for __tmp3 in range(bit_flip_code.n):
                decoded, traced_out_state = __tmp2(
                    bit_flip_code, __tmp5, __tmp6, __tmp3
                )
                assert decoded == __tmp5
                np.testing.assert_allclose(traced_out_state_no_error, traced_out_state, atol=1e-6)

    # Test that we cannot correct a Z error. In this case, they manifest as a phase error, so we
    # test the state vectors.
    _, traced_out_state_no_error = __tmp2(
        bit_flip_code, __tmp5=1, __tmp6=None, __tmp3=None
    )
    _, traced_out_state_z1_error = __tmp2(
        bit_flip_code, __tmp5=1, __tmp6=cirq.Z, __tmp3=1
    )

    with np.testing.assert_raises(AssertionError):
        np.testing.assert_allclose(traced_out_state_no_error, traced_out_state_z1_error, atol=1e-6)
