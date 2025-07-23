from typing import TypeAlias
__typ0 : TypeAlias = "str"
# pylint: disable=wrong-or-nonexistent-copyright-notice
from typing import List, Mapping, Sequence

import collections
import time

import numpy as np
import matplotlib.pyplot as plt
import sympy

import cirq


class LivePlotCollector(cirq.Collector):
    """Performs concurrent collection of a parameter sweep over a circuit.

    Purposefully breaks down the sweep into individual calls, in order to test
    how samplers reacts to being given asynchronous sweeps to perform in
    parallel.

    Draws results live as they wait, start, and complete. (Note that this tends
    to slow things down quite a lot, so refreshes are limited to 5Hz.)
    """

    def __tmp5(
        __tmp0, *, circuit, __tmp3, __tmp6, repetitions: <FILL>
    ):
        __tmp0.next_index = 0
        __tmp0.circuit = circuit
        __tmp0.sweep = cirq.Points(__tmp3, __tmp6)
        __tmp0.resolvers = list(cirq.to_resolvers(__tmp0.sweep))
        __tmp0.reps = repetitions

        __tmp0.unstarted_xs = list(__tmp6)
        __tmp0.started_xs: List[float] = []
        __tmp0.result_xs: List[float] = []
        __tmp0.result_ys: Mapping[__typ0, List[float]] = collections.defaultdict(list)

        __tmp0.fig = plt.figure()
        __tmp0.last_redraw_time = time.monotonic()

    def __tmp7(__tmp0):
        if __tmp0.next_index >= len(__tmp0.sweep):
            return None
        k = __tmp0.next_index
        p = __tmp0.sweep.points[k]
        __tmp0.next_index += 1
        __tmp0.started_xs.append(p)
        __tmp0.unstarted_xs.remove(p)
        return cirq.CircuitSampleJob(
            cirq.resolve_parameters(__tmp0.circuit, __tmp0.resolvers[k]), repetitions=__tmp0.reps, tag=p
        )

    def _redraw(__tmp0):
        __tmp0.fig.clear()
        plt.scatter(__tmp0.unstarted_xs, [0] * len(__tmp0.unstarted_xs), label='unstarted', s=1)
        plt.scatter(__tmp0.started_xs, [1] * len(__tmp0.started_xs), label='started', s=1)
        for k, v in __tmp0.result_ys.items():
            plt.scatter(__tmp0.result_xs, v, label=k, s=1)
        plt.xlabel(__tmp0.sweep.key)
        plt.legend()
        __tmp0.fig.canvas.draw()
        plt.pause(0.00001)

    def on_job_result(__tmp0, __tmp1, __tmp4):
        __tmp0.started_xs.remove(__tmp1.tag)
        __tmp0.result_xs.append(__tmp1.tag)
        for k, v in __tmp4.measurements.items():
            __tmp0.result_ys[k].append(np.mean(v.reshape(v.size)))

        t = time.monotonic()
        if t > __tmp0.last_redraw_time + 0.2 or not __tmp0.started_xs:
            __tmp0.last_redraw_time = t
            __tmp0._redraw()


def __tmp2():
    a, b = cirq.LineQubit.range(2)

    sampler = cirq.Simulator()

    circuit = cirq.Circuit(
        cirq.X(a) ** sympy.Symbol('t'),
        cirq.CNOT(a, b) ** sympy.Symbol('t'),
        cirq.measure(a, key='leader'),
        cirq.measure(b, key='follower'),
    )

    collector = LivePlotCollector(
        circuit=circuit, __tmp3='t', __tmp6=np.linspace(0, 1, 1000), repetitions=200
    )

    collector.collect(sampler, concurrency=5)
    plt.show()


if __name__ == '__main__':
    __tmp2()
