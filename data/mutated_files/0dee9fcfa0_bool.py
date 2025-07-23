from typing import TypeAlias
__typ0 : TypeAlias = "str"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[__typ0, Any]


class Rule:
    APP = 'app'
    WEB = 'web'

    def __init__(self, values) -> None:
        if 'id' in values:
            self.id = values['id']
            del values['id']
        else:
            self.id = __typ0(uuid.uuid4())
        self.values = values

    def to_json(self) -> Any:
        return self.values

    def __iter__(self) -> Iterator[Dict[__typ0, __typ0]]:
        return iter(self.to_json())

    def __getitem__(self, item: __typ0) -> __typ0:
        return self.values[item]

    def __contains__(self, item: __typ0) -> bool:
        return item in self.values

    def __len__(self) -> int:
        return len(self.values)

    def is_web(self) -> bool:
        return self.values['type'] == Rule.WEB

    def is_app(self) -> bool:
        return self.values['type'] == Rule.APP


class Project:
    @staticmethod
    def reinstate(config_project: Any) -> 'Project':
        return Project(config_project['name'],
                       [Rule(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project: __typ0) -> 'Project':
        return Project(none_project, [])

    def __init__(self, name, rules: List[Rule]) -> None:
        self.rules = rules
        self.name = name

    def to_json(self) -> Any:
        return {
            'name': self.name,
            'rules': [rule.to_json() for rule in self.rules]
        }


class Projects:
    @staticmethod
    def reinstate(__tmp0: List[Any], none_project: __typ0) :
        projects: List['Project'] = []
        for config_project in __tmp0:
            rules = [Rule(rule) for rule in config_project['rules']]
            project = Project(config_project['name'], rules)
            projects.append(project)

        return Projects(projects, none_project)

    def __init__(self, projects: List[Project], none_project: __typ0) -> None:
        self.none_project = none_project
        self.projects = projects
        self.projects.append(Project.create_empty(self.none_project))

    def __iter__(self) -> Iterator[Project]:
        return iter(self.projects)

    def __len__(self) -> int:
        return len(self.projects)

    def to_json(self) -> Any:
        return [project.to_json() for project in self.projects
                if project.name != self.none_project]


class Config:
    config: ConfigDict

    @staticmethod
    def parse(values: ConfigDict) -> 'Config':
        port = int(values['daemon']['port'])
        host = __typ0(values['daemon']['host'])
        interval = int(values['gui']['interval'])
        run_daemon = bool(values['gui']['run_daemon'])
        start_day_time = __typ0(values['gui']['start_day_time'])
        projects = Projects.reinstate(
            values['gui']['projects'],
            __typ0(uuid.uuid4())
        )
        return Config(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __init__(self, port: int, host: __typ0, interval: int, run_daemon: <FILL>,
                 start_day_time: __typ0, projects: Projects) -> None:
        self.port = port
        self.host = host
        self.interval = interval
        self.run_daemon = run_daemon
        self.start_day_time = start_day_time
        self.projects = projects

    def modify(self, port: int, host, interval: int, run_daemon: bool,
               projects: List[Project]) -> 'Config':
        return Config(port, host, interval, run_daemon, self.start_day_time,
                      Projects(projects, self.projects.none_project))

    def get_full_address(self) :
        return '%s:%s' % (self.host, self.port)
