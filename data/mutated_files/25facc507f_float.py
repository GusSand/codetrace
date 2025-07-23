# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import Sequence

import cirq
import cirq.work as cw
import numpy as np


class __typ0(cirq.NoiseModel):
    """This simulates asymmetric readout error.

    The noise is structured so the T1 decay is applied, then the readout bitflip, then measurement.
    If a circuit contains measurements, they must be in moments that don't also contain gates.
    """

    def __init__(__tmp1, depol_prob: <FILL>, __tmp2, __tmp3):
        __tmp1.qubit_noise_gate = cirq.DepolarizingChannel(depol_prob)
        __tmp1.readout_noise_gate = cirq.BitFlipChannel(__tmp2)
        __tmp1.readout_decay_gate = cirq.AmplitudeDampingChannel(__tmp3)

    def noisy_moment(__tmp1, __tmp0, system_qubits):
        if cirq.devices.noise_model.validate_all_measurements(__tmp0):
            return [
                cirq.Moment(__tmp1.readout_decay_gate(q) for q in system_qubits),
                cirq.Moment(__tmp1.readout_noise_gate(q) for q in system_qubits),
                __tmp0,
            ]
        else:
            return [__tmp0, cirq.Moment(__tmp1.qubit_noise_gate(q) for q in system_qubits)]


def test_calibrate_readout_error():
    sampler = cirq.DensityMatrixSimulator(
        noise=__typ0(
            depol_prob=1e-3,
            __tmp2=0.03,
            __tmp3=0.03,
        ),
        seed=10,
    )
    readout_calibration = cw.calibrate_readout_error(
        qubits=cirq.LineQubit.range(2),
        sampler=sampler,
        stopping_criteria=cw.RepetitionsStoppingCriteria(100_000),
    )
    means = readout_calibration.means()
    assert len(means) == 2, 'Two qubits'
    assert np.all(means > 0.89)
    assert np.all(means < 0.91)
