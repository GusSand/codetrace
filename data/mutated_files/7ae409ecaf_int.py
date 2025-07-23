# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import cast, List, Optional

import numpy as np
import pytest

import cirq

import examples.stabilizer_code as sc


def __tmp3(
    code,
    __tmp5: <FILL>,
    error_gate,
    __tmp4: int,
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

    if error_gate:
        circuit.append(error_gate(qubits[__tmp4]))

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


def __tmp1():
    # Table 3.2.
    five_qubit_code = sc.StabilizerCode(
        group_generators=['XZZXI', 'IXZZX', 'XIXZZ', 'ZXIXZ'], correctable_errors=['X', 'Z']
    )

    for __tmp5 in [0, 1]:
        decoded, _ = __tmp3(
            five_qubit_code, __tmp5, error_gate=None, __tmp4=None
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
def __tmp0(group_generators):
    code = sc.StabilizerCode(group_generators=group_generators, correctable_errors=['X', 'Z'])

    for __tmp5 in [0, 1]:
        _, traced_out_state_no_error = __tmp3(
            code, __tmp5, error_gate=None, __tmp4=None
        )

        for error_gate in [cirq.X, cirq.Z]:
            for __tmp4 in range(code.n):
                decoded, traced_out_state = __tmp3(
                    code, __tmp5, error_gate, __tmp4
                )
                assert decoded == __tmp5
                np.testing.assert_allclose(traced_out_state_no_error, traced_out_state, atol=1e-6)


def __tmp2():
    # Also known as the bit-flip code.
    bit_flip_code = sc.StabilizerCode(group_generators=['ZZI', 'ZIZ'], correctable_errors=['X'])

    for __tmp5 in [0, 1]:
        _, traced_out_state_no_error = __tmp3(
            bit_flip_code, __tmp5, error_gate=None, __tmp4=None
        )

        for error_gate in [cirq.X]:
            for __tmp4 in range(bit_flip_code.n):
                decoded, traced_out_state = __tmp3(
                    bit_flip_code, __tmp5, error_gate, __tmp4
                )
                assert decoded == __tmp5
                np.testing.assert_allclose(traced_out_state_no_error, traced_out_state, atol=1e-6)

    # Test that we cannot correct a Z error. In this case, they manifest as a phase error, so we
    # test the state vectors.
    _, traced_out_state_no_error = __tmp3(
        bit_flip_code, __tmp5=1, error_gate=None, __tmp4=None
    )
    _, traced_out_state_z1_error = __tmp3(
        bit_flip_code, __tmp5=1, error_gate=cirq.Z, __tmp4=1
    )

    with np.testing.assert_raises(AssertionError):
        np.testing.assert_allclose(traced_out_state_no_error, traced_out_state_z1_error, atol=1e-6)
