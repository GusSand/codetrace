from .event import Event


class __typ0(Event):
    project: str
    rule_id: str

    def __init__(__tmp0, project: <FILL>, rule_id, event) :
        super().__init__(event, event.type)
        __tmp0.rule_id = rule_id
        __tmp0.project = project
