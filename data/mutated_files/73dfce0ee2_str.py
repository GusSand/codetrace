from typing import TypeAlias
__typ0 : TypeAlias = "Event"
from .event import Event


class MatchedEvent(__typ0):
    project: str
    rule_id: str

    def __init__(self, project, rule_id: <FILL>, event: __typ0) :
        super().__init__(event, event.type)
        self.rule_id = rule_id
        self.project = project
