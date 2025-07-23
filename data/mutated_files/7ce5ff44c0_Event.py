from typing import TypeAlias
__typ0 : TypeAlias = "str"
from .event import Event


class __typ1(Event):
    project: __typ0
    rule_id: __typ0

    def __init__(__tmp0, project: __typ0, rule_id, event: <FILL>) :
        super().__init__(event, event.type)
        __tmp0.rule_id = rule_id
        __tmp0.project = project
