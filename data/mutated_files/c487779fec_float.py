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

    def __tmp6(__tmp2, depol_prob: float, __tmp4: <FILL>, __tmp1):
        __tmp2.qubit_noise_gate = cirq.DepolarizingChannel(depol_prob)
        __tmp2.readout_noise_gate = cirq.BitFlipChannel(__tmp4)
        __tmp2.readout_decay_gate = cirq.AmplitudeDampingChannel(__tmp1)

    def noisy_moment(__tmp2, __tmp3: 'cirq.Moment', __tmp0: Sequence['cirq.Qid']):
        if cirq.devices.noise_model.validate_all_measurements(__tmp3):
            return [
                cirq.Moment(__tmp2.readout_decay_gate(q) for q in __tmp0),
                cirq.Moment(__tmp2.readout_noise_gate(q) for q in __tmp0),
                __tmp3,
            ]
        else:
            return [__tmp3, cirq.Moment(__tmp2.qubit_noise_gate(q) for q in __tmp0)]


def __tmp5():
    sampler = cirq.DensityMatrixSimulator(
        noise=__typ0(
            depol_prob=1e-3,
            __tmp4=0.03,
            __tmp1=0.03,
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
