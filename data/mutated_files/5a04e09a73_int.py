from typing import TypeAlias
__typ0 : TypeAlias = "bool"
from protoactor.persistence.messages import PersistedEvent
from protoactor.persistence.snapshot_strategies.abstract_snapshot_strategy import AbstractSnapshotStrategy


class IntervalStrategy(AbstractSnapshotStrategy):
    def __init__(self, __tmp0: <FILL>):
        self._events_per_snapshot = __tmp0

    def should_take_snapshot(self, persisted_event: PersistedEvent) :
        return persisted_event.index % self._events_per_snapshot == 0