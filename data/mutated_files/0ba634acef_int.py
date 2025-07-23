# pylint: disable=wrong-or-nonexistent-copyright-notice
""" Shor's code is a stabilizer code for quantum error correction.
It uses 9 qubits to encode 1 logic qubit and is able to correct
at most one bit flip and one sign flip or their combination.

(0, 0): ───@───@───H───@───@───@───@───X───H───@───@───X───M───
           │   │       │   │   │   │   │       │   │   │
(0, 1): ───┼───┼───────X───┼───X───┼───@───────┼───┼───┼───M───
           │   │           │       │   │       │   │   │
(0, 2): ───┼───┼───────────X───────X───@───────┼───┼───┼───M───
           │   │                               │   │   │
(0, 3): ───X───┼───H───@───@───@───@───X───H───X───┼───@───M───
               │       │   │   │   │   │           │   │
(0, 4): ───────┼───────X───┼───X───┼───@───────────┼───┼───M───
               │           │       │   │           │   │
(0, 5): ───────┼───────────X───────X───@───────────┼───┼───M───
               │                                   │   │
(0, 6): ───────X───H───@───@───@───@───X───H───────X───@───M───
                       │   │   │   │   │
(0, 7): ───────────────X───┼───X───┼───@───────────────────M───
                           │       │   │
(0, 8): ───────────────────X───────X───@───────────────────M───

reference: P. W. Shor, Phys. Rev. A, 52, R2493 (1995).
"""

import random

import cirq


class __typ0:
    def __init__(__tmp0):
        __tmp0.num_physical_qubits = 9
        __tmp0.physical_qubits = cirq.LineQubit.range(__tmp0.num_physical_qubits)

    def encode(__tmp0):
        yield cirq.ops.Moment([cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[3])])
        yield cirq.ops.Moment([cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[6])])
        yield cirq.ops.Moment(
            [
                cirq.H(__tmp0.physical_qubits[0]),
                cirq.H(__tmp0.physical_qubits[3]),
                cirq.H(__tmp0.physical_qubits[6]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[1]),
                cirq.CNOT(__tmp0.physical_qubits[3], __tmp0.physical_qubits[4]),
                cirq.CNOT(__tmp0.physical_qubits[6], __tmp0.physical_qubits[7]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[2]),
                cirq.CNOT(__tmp0.physical_qubits[3], __tmp0.physical_qubits[5]),
                cirq.CNOT(__tmp0.physical_qubits[6], __tmp0.physical_qubits[8]),
            ]
        )

    def apply_gate(__tmp0, gate: cirq.Gate, __tmp1: <FILL>):
        if __tmp1 > __tmp0.num_physical_qubits:
            raise IndexError
        else:
            return gate(__tmp0.physical_qubits[__tmp1])

    def correct(__tmp0):
        yield cirq.ops.Moment(
            [
                cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[1]),
                cirq.CNOT(__tmp0.physical_qubits[3], __tmp0.physical_qubits[4]),
                cirq.CNOT(__tmp0.physical_qubits[6], __tmp0.physical_qubits[7]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[2]),
                cirq.CNOT(__tmp0.physical_qubits[3], __tmp0.physical_qubits[5]),
                cirq.CNOT(__tmp0.physical_qubits[6], __tmp0.physical_qubits[8]),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.CCNOT(
                    __tmp0.physical_qubits[1], __tmp0.physical_qubits[2], __tmp0.physical_qubits[0]
                ),
                cirq.CCNOT(
                    __tmp0.physical_qubits[4], __tmp0.physical_qubits[5], __tmp0.physical_qubits[3]
                ),
                cirq.CCNOT(
                    __tmp0.physical_qubits[7], __tmp0.physical_qubits[8], __tmp0.physical_qubits[6]
                ),
            ]
        )
        yield cirq.ops.Moment(
            [
                cirq.H(__tmp0.physical_qubits[0]),
                cirq.H(__tmp0.physical_qubits[3]),
                cirq.H(__tmp0.physical_qubits[6]),
            ]
        )
        yield cirq.ops.Moment([cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[3])])
        yield cirq.ops.Moment([cirq.CNOT(__tmp0.physical_qubits[0], __tmp0.physical_qubits[6])])
        yield cirq.ops.Moment(
            [cirq.CCNOT(__tmp0.physical_qubits[3], __tmp0.physical_qubits[6], __tmp0.physical_qubits[0])]
        )


if __name__ == '__main__':
    # coverage: ignore

    # create circuit with 9 physical qubits
    code = __typ0()

    circuit = cirq.Circuit(code.apply_gate(cirq.X ** (1 / 4), 0))
    print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    circuit += cirq.Circuit(code.encode())
    print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    # create error
    circuit += cirq.Circuit(
        code.apply_gate(cirq.X, random.randint(0, code.num_physical_qubits - 1))
    )
    print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))

    # correct error and decode
    circuit += cirq.Circuit(code.correct())
    print(cirq.dirac_notation(circuit.final_state_vector(initial_state=0)))
