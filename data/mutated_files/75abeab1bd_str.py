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

    def __tmp6(
        __tmp2, *, circuit, __tmp4: <FILL>, __tmp7: Sequence[float], __tmp0: int
    ):
        __tmp2.next_index = 0
        __tmp2.circuit = circuit
        __tmp2.sweep = cirq.Points(__tmp4, __tmp7)
        __tmp2.resolvers = list(cirq.to_resolvers(__tmp2.sweep))
        __tmp2.reps = __tmp0

        __tmp2.unstarted_xs = list(__tmp7)
        __tmp2.started_xs: List[float] = []
        __tmp2.result_xs: List[float] = []
        __tmp2.result_ys: Mapping[str, List[float]] = collections.defaultdict(list)

        __tmp2.fig = plt.figure()
        __tmp2.last_redraw_time = time.monotonic()

    def next_job(__tmp2):
        if __tmp2.next_index >= len(__tmp2.sweep):
            return None
        k = __tmp2.next_index
        p = __tmp2.sweep.points[k]
        __tmp2.next_index += 1
        __tmp2.started_xs.append(p)
        __tmp2.unstarted_xs.remove(p)
        return cirq.CircuitSampleJob(
            cirq.resolve_parameters(__tmp2.circuit, __tmp2.resolvers[k]), __tmp0=__tmp2.reps, tag=p
        )

    def _redraw(__tmp2):
        __tmp2.fig.clear()
        plt.scatter(__tmp2.unstarted_xs, [0] * len(__tmp2.unstarted_xs), label='unstarted', s=1)
        plt.scatter(__tmp2.started_xs, [1] * len(__tmp2.started_xs), label='started', s=1)
        for k, v in __tmp2.result_ys.items():
            plt.scatter(__tmp2.result_xs, v, label=k, s=1)
        plt.xlabel(__tmp2.sweep.key)
        plt.legend()
        __tmp2.fig.canvas.draw()
        plt.pause(0.00001)

    def __tmp1(__tmp2, __tmp3, __tmp5):
        __tmp2.started_xs.remove(__tmp3.tag)
        __tmp2.result_xs.append(__tmp3.tag)
        for k, v in __tmp5.measurements.items():
            __tmp2.result_ys[k].append(np.mean(v.reshape(v.size)))

        t = time.monotonic()
        if t > __tmp2.last_redraw_time + 0.2 or not __tmp2.started_xs:
            __tmp2.last_redraw_time = t
            __tmp2._redraw()


def example():
    a, b = cirq.LineQubit.range(2)

    sampler = cirq.Simulator()

    circuit = cirq.Circuit(
        cirq.X(a) ** sympy.Symbol('t'),
        cirq.CNOT(a, b) ** sympy.Symbol('t'),
        cirq.measure(a, key='leader'),
        cirq.measure(b, key='follower'),
    )

    collector = LivePlotCollector(
        circuit=circuit, __tmp4='t', __tmp7=np.linspace(0, 1, 1000), __tmp0=200
    )

    collector.collect(sampler, concurrency=5)
    plt.show()


if __name__ == '__main__':
    example()
