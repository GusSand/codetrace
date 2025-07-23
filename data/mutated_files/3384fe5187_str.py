from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

__typ1 = Dict[str, __typ3]


class Rule:
    APP = 'app'
    WEB = 'web'

    def __init__(self, values) :
        if 'id' in values:
            self.id = values['id']
            del values['id']
        else:
            self.id = str(uuid.uuid4())
        self.values = values

    def to_json(self) :
        return self.values

    def __iter__(self) :
        return iter(self.to_json())

    def __tmp0(self, item) :
        return self.values[item]

    def __contains__(self, item) :
        return item in self.values

    def __len__(self) :
        return len(self.values)

    def is_web(self) :
        return self.values['type'] == Rule.WEB

    def is_app(self) :
        return self.values['type'] == Rule.APP


class __typ4:
    @staticmethod
    def reinstate(config_project) :
        return __typ4(config_project['name'],
                       [Rule(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project: str) :
        return __typ4(none_project, [])

    def __init__(self, name, rules) -> None:
        self.rules = rules
        self.name = name

    def to_json(self) :
        return {
            'name': self.name,
            'rules': [rule.to_json() for rule in self.rules]
        }


class Projects:
    @staticmethod
    def reinstate(config_projects, none_project) :
        projects: List['Project'] = []
        for config_project in config_projects:
            rules = [Rule(rule) for rule in config_project['rules']]
            project = __typ4(config_project['name'], rules)
            projects.append(project)

        return Projects(projects, none_project)

    def __init__(self, projects, none_project: <FILL>) -> None:
        self.none_project = none_project
        self.projects = projects
        self.projects.append(__typ4.create_empty(self.none_project))

    def __iter__(self) -> Iterator[__typ4]:
        return iter(self.projects)

    def __len__(self) :
        return len(self.projects)

    def to_json(self) :
        return [project.to_json() for project in self.projects
                if project.name != self.none_project]


class Config:
    config: __typ1

    @staticmethod
    def parse(values) :
        port = __typ0(values['daemon']['port'])
        host = str(values['daemon']['host'])
        interval = __typ0(values['gui']['interval'])
        run_daemon = __typ2(values['gui']['run_daemon'])
        start_day_time = str(values['gui']['start_day_time'])
        projects = Projects.reinstate(
            values['gui']['projects'],
            str(uuid.uuid4())
        )
        return Config(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __init__(self, port, host, interval, run_daemon,
                 start_day_time, projects) :
        self.port = port
        self.host = host
        self.interval = interval
        self.run_daemon = run_daemon
        self.start_day_time = start_day_time
        self.projects = projects

    def modify(self, port, host, interval, run_daemon,
               projects) :
        return Config(port, host, interval, run_daemon, self.start_day_time,
                      Projects(projects, self.projects.none_project))

    def get_full_address(self) :
        return '%s:%s' % (self.host, self.port)
