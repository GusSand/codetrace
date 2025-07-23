# pylint: disable=wrong-or-nonexistent-copyright-notice
"""Contains functions for adding JSON serialization and de-serialization for
classes in Contrib.

"""

from cirq.protocols.json_serialization import DEFAULT_RESOLVERS


def __tmp1(__tmp0: <FILL>):
    """Extend cirq's JSON API with resolvers for cirq contrib classes."""
    from cirq.contrib.quantum_volume import QuantumVolumeResult
    from cirq.contrib.acquaintance import SwapPermutationGate

    classes = [
        QuantumVolumeResult,
        SwapPermutationGate,
    ]
    d = {cls.__name__: cls for cls in classes}
    return d.get(__tmp0, None)


DEFAULT_CONTRIB_RESOLVERS = [__tmp1] + DEFAULT_RESOLVERS
