from typing import TypeAlias
__typ0 : TypeAlias = "float"
# Copyright 2022 The Cirq Developers
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

import numpy as np
import cirq
import pytest

from cirq.experiments.single_qubit_readout_calibration_test import NoisySingleQubitReadoutSampler


def __tmp3(__tmp6: <FILL>, __tmp5: __typ0, __tmp8):
    expected_cm = np.zeros((2 ** __tmp6,) * 2)
    for i in range(2 ** __tmp6):
        for j in range(2 ** __tmp6):
            p = 1.0
            for k in range(__tmp6):
                b0 = (i >> k) & 1
                b1 = (j >> k) & 1
                if b0 == 0:
                    p *= __tmp5 * b1 + (1 - __tmp5) * (1 - b1)
                else:
                    p *= __tmp8 * (1 - b1) + (1 - __tmp8) * b1
            expected_cm[i][j] = p
    return expected_cm


@pytest.mark.parametrize('p0, p1', [(0, 0), (0.2, 0.4), (0.5, 0.5), (0.6, 0.3), (1.0, 1.0)])
def __tmp4(__tmp5, __tmp8):
    sampler = NoisySingleQubitReadoutSampler(__tmp5, __tmp8, seed=1234)
    __tmp6 = 4
    qubits = cirq.LineQubit.range(__tmp6)
    expected_cm = __tmp3(__tmp6, __tmp5, __tmp8)
    qubits_small = qubits[:2]
    expected_cm_small = __tmp3(2, __tmp5, __tmp8)
    repetitions = 12_000
    # Build entire confusion matrix by running 2 ** 4 = 16 circuits.
    readout_cm = cirq.measure_confusion_matrix(sampler, qubits, repetitions=repetitions)
    assert readout_cm.repetitions == repetitions
    for q, expected in zip([None, qubits_small], [expected_cm, expected_cm_small]):
        np.testing.assert_allclose(readout_cm.confusion_matrix(q), expected, atol=1e-2)
        np.testing.assert_allclose(
            readout_cm.confusion_matrix(q) @ readout_cm.correction_matrix(q),
            np.eye(expected.shape[0]),
            atol=1e-2,
        )

    # Build a tensored confusion matrix using smaller single qubit confusion matrices.
    # This works because the error is uncorrelated and requires only 4 * 2 = 8 circuits.
    readout_cm = cirq.measure_confusion_matrix(
        sampler, [[q] for q in qubits], repetitions=repetitions
    )
    assert readout_cm.repetitions == repetitions
    for q, expected in zip([None, qubits_small], [expected_cm, expected_cm_small]):
        np.testing.assert_allclose(readout_cm.confusion_matrix(q), expected, atol=1e-2)
        np.testing.assert_allclose(
            readout_cm.confusion_matrix(q) @ readout_cm.correction_matrix(q),
            np.eye(expected.shape[0]),
            atol=1e-2,
        )

    # Apply corrections to sampled probabilities using readout_cm.
    qs = qubits_small
    circuit = cirq.Circuit(cirq.H.on_each(*qs), cirq.measure(*qs))
    reps = 100_000
    sampled_result = cirq.get_state_histogram(sampler.run(circuit, repetitions=reps)) / reps
    expected_result = [1 / 4] * 4

    def __tmp2(__tmp1: np.ndarray):
        return np.sum((expected_result - __tmp1) ** 2)

    corrected_result = readout_cm.apply(sampled_result, qs)
    assert __tmp2(corrected_result) <= __tmp2(sampled_result)


def __tmp0():
    __tmp6 = 2
    confusion_matrix = __tmp3(__tmp6, 0.1, 0.2)
    qubits = cirq.LineQubit.range(4)
    with pytest.raises(ValueError, match=r"measure_qubits cannot be empty"):
        _ = cirq.TensoredConfusionMatrices([], [], repetitions=0, timestamp=0)

    with pytest.raises(ValueError, match=r"len\(confusion_matrices\)"):
        _ = cirq.TensoredConfusionMatrices(
            [confusion_matrix], [qubits[:2], qubits[2:]], repetitions=0, timestamp=0
        )

    with pytest.raises(ValueError, match="Shape mismatch for confusion matrix"):
        _ = cirq.TensoredConfusionMatrices(confusion_matrix, qubits, repetitions=0, timestamp=0)

    with pytest.raises(ValueError, match="Repeated qubits not allowed"):
        _ = cirq.TensoredConfusionMatrices(
            [confusion_matrix, confusion_matrix],
            [qubits[:2], qubits[1:3]],
            repetitions=0,
            timestamp=0,
        )

    readout_cm = cirq.TensoredConfusionMatrices(
        [confusion_matrix, confusion_matrix], [qubits[:2], qubits[2:]], repetitions=0, timestamp=0
    )

    with pytest.raises(ValueError, match="should be a subset of"):
        _ = readout_cm.confusion_matrix([cirq.NamedQubit("a")])

    with pytest.raises(ValueError, match="should be a subset of"):
        _ = readout_cm.correction_matrix([cirq.NamedQubit("a")])

    with pytest.raises(ValueError, match="result.shape .* should be"):
        _ = readout_cm.apply(np.asarray([100]), qubits[:2])

    with pytest.raises(ValueError, match="method.* should be"):
        _ = readout_cm.apply(np.asarray([1 / 16] * 16), method='l1norm')


def __tmp7():
    mat1 = cirq.testing.random_orthogonal(4, random_state=1234)
    mat2 = cirq.testing.random_orthogonal(2, random_state=1234)
    q = cirq.LineQubit.range(3)
    a = cirq.TensoredConfusionMatrices([mat1, mat2], [q[:2], q[2:]], repetitions=0, timestamp=0)
    b = cirq.TensoredConfusionMatrices(mat1, q[:2], repetitions=0, timestamp=0)
    c = cirq.TensoredConfusionMatrices(mat2, q[2:], repetitions=0, timestamp=0)
    for x in [a, b, c]:
        cirq.testing.assert_equivalent_repr(x)
        assert cirq.approx_eq(x, x)
        assert x._approx_eq_(mat1, 1e-6) is NotImplemented
    eq = cirq.testing.EqualsTester()
    eq.add_equality_group(a, a)
    eq.add_equality_group(b, b)
    eq.add_equality_group(c, c)
