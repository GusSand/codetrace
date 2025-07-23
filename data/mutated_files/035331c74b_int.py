# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import cast
import numpy as np
import pytest
import sympy

import cirq
import cirq_google.optimizers.convert_to_sqrt_iswap as cgoc
import cirq_google as cig


def __tmp2(__tmp7, __tmp0):
    unitary1 = cirq.unitary(__tmp7)
    unitary2 = cirq.unitary(__tmp0)
    if unitary2.size == 1:
        # Resize the unitary of empty circuits to be 4x4 for 2q gates
        unitary2 = unitary2 * np.eye(unitary1.shape[0])
    return cirq.allclose_up_to_global_phase(unitary1, unitary2)


@pytest.mark.parametrize(
    'gate, expected_length',
    [
        (cast(cirq.Gate, cirq.ISWAP), 7),  # cast is for fixing mypy confusion
        (cirq.CZ, 8),
        (cirq.SWAP, 7),
        (cirq.CNOT, 9),
        (cirq.ISWAP ** 0.5, 1),
        (cirq.ISWAP ** -0.5, 1),
        (cirq.ISwapPowGate(exponent=0.5), 1),
        (cirq.ISwapPowGate(exponent=-0.5), 1),
        (cirq.FSimGate(theta=np.pi / 4, phi=0), 1),
        *[(cirq.SwapPowGate(exponent=a), 13) for a in np.linspace(0, 2 * np.pi, 20)],
        *[(cirq.CZPowGate(exponent=a), 8) for a in np.linspace(0, 2 * np.pi, 20)],
        *[(cirq.ISwapPowGate(exponent=a), 5) for a in np.linspace(0, 2 * np.pi, 20)],
        *[(cirq.CNotPowGate(exponent=a), 9) for a in np.linspace(0, 2 * np.pi, 20)],
        *[(cirq.FSimGate(theta=a, phi=a), 13) for a in np.linspace(0, 2 * np.pi, 20)],
    ],
)
def test_two_qubit_gates(__tmp4, __tmp1: <FILL>):
    """Tests that two qubit gates decompose to an equivalent and
    serializable circuit with the expected length (or less).
    """
    q0 = cirq.GridQubit(5, 3)
    q1 = cirq.GridQubit(5, 4)
    original_circuit = cirq.Circuit(__tmp4(q0, q1))
    converted_circuit = original_circuit.copy()
    cgoc.ConvertToSqrtIswapGates().optimize_circuit(converted_circuit)
    cig.SQRT_ISWAP_GATESET.serialize(converted_circuit)
    assert len(converted_circuit) <= __tmp1
    assert __tmp2(original_circuit, converted_circuit)


@pytest.mark.parametrize(
    'gate, expected_length',
    [
        (cirq.FSimGate(theta=sympy.Symbol('t'), phi=0), 8),
        (cirq.FSimGate(theta=0, phi=sympy.Symbol('t')), 8),
        (cirq.ISwapPowGate(exponent=sympy.Symbol('t')), 5),
        (cirq.SwapPowGate(exponent=sympy.Symbol('t')), 13),
        (cirq.CNotPowGate(exponent=sympy.Symbol('t')), 9),
        (cirq.CZPowGate(exponent=sympy.Symbol('t')), 8),
    ],
)
def __tmp3(__tmp4, __tmp1: int):
    """Tests that the gates with symbols decompose without error into a
    circuit that has an equivalent unitary form.
    """
    q0 = cirq.GridQubit(5, 3)
    q1 = cirq.GridQubit(5, 4)
    original_circuit = cirq.Circuit(__tmp4(q0, q1))
    converted_circuit = original_circuit.copy()
    cgoc.ConvertToSqrtIswapGates().optimize_circuit(converted_circuit)
    assert len(converted_circuit) <= __tmp1

    # Check if unitaries are the same
    for val in np.linspace(0, 2 * np.pi, 12):
        assert __tmp2(
            cirq.resolve_parameters(original_circuit, {'t': val}),
            cirq.resolve_parameters(converted_circuit, {'t': val}),
        )


def __tmp6():
    """Test if the sqrt_iswap synthesis for a cphase rotation is correct"""
    thetas = np.linspace(0, 2 * np.pi, 100)
    qubits = [cirq.NamedQubit('a'), cirq.NamedQubit('b')]
    for theta in thetas:
        expected = cirq.CZPowGate(exponent=theta)
        decomposition = cgoc.cphase_to_sqrt_iswap(qubits[0], qubits[1], theta)
        actual = cirq.Circuit(decomposition)
        expected_unitary = cirq.unitary(expected)
        actual_unitary = cirq.unitary(actual)
        np.testing.assert_allclose(expected_unitary, actual_unitary, atol=1e-07)


def __tmp5():
    """Test if the sqrt_iswap synthesis for a givens rotation is correct"""
    thetas = np.linspace(0, 2 * np.pi, 100)
    qubits = [cirq.NamedQubit('a'), cirq.NamedQubit('b')]
    for theta in thetas:
        program = cirq.Circuit(cirq.givens(theta).on(qubits[0], qubits[1]))
        unitary = cirq.unitary(program)
        test_program = program.copy()
        cgoc.ConvertToSqrtIswapGates().optimize_circuit(test_program)
        test_unitary = cirq.unitary(test_program)
        np.testing.assert_allclose(
            4, np.abs(np.trace(np.conjugate(np.transpose(test_unitary)) @ unitary))
        )


def __tmp8():
    class ThreeQubitGate(cirq.testing.ThreeQubitGate):
        pass

    q0 = cirq.LineQubit(0)
    q1 = cirq.LineQubit(1)
    q2 = cirq.LineQubit(2)
    circuit = cirq.Circuit(ThreeQubitGate()(q0, q1, q2))

    with pytest.raises(TypeError):
        cgoc.ConvertToSqrtIswapGates().optimize_circuit(circuit)
