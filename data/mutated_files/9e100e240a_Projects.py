from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[__typ1, __typ3]


class Rule:
    APP = 'app'
    WEB = 'web'

    def __tmp1(__tmp0, values: Dict[__typ1, __typ1]) :
        if 'id' in values:
            __tmp0.id = values['id']
            del values['id']
        else:
            __tmp0.id = __typ1(uuid.uuid4())
        __tmp0.values = values

    def to_json(__tmp0) :
        return __tmp0.values

    def __iter__(__tmp0) -> Iterator[Dict[__typ1, __typ1]]:
        return iter(__tmp0.to_json())

    def __getitem__(__tmp0, item: __typ1) :
        return __tmp0.values[item]

    def __contains__(__tmp0, item: __typ1) -> __typ2:
        return item in __tmp0.values

    def __len__(__tmp0) -> __typ0:
        return len(__tmp0.values)

    def is_web(__tmp0) :
        return __tmp0.values['type'] == Rule.WEB

    def is_app(__tmp0) :
        return __tmp0.values['type'] == Rule.APP


class Project:
    @staticmethod
    def reinstate(config_project: __typ3) -> 'Project':
        return Project(config_project['name'],
                       [Rule(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project) :
        return Project(none_project, [])

    def __tmp1(__tmp0, name, rules: List[Rule]) -> None:
        __tmp0.rules = rules
        __tmp0.name = name

    def to_json(__tmp0) :
        return {
            'name': __tmp0.name,
            'rules': [rule.to_json() for rule in __tmp0.rules]
        }


class Projects:
    @staticmethod
    def reinstate(config_projects: List[__typ3], none_project: __typ1) -> 'Projects':
        projects: List['Project'] = []
        for config_project in config_projects:
            rules = [Rule(rule) for rule in config_project['rules']]
            project = Project(config_project['name'], rules)
            projects.append(project)

        return Projects(projects, none_project)

    def __tmp1(__tmp0, projects, none_project) -> None:
        __tmp0.none_project = none_project
        __tmp0.projects = projects
        __tmp0.projects.append(Project.create_empty(__tmp0.none_project))

    def __iter__(__tmp0) :
        return iter(__tmp0.projects)

    def __len__(__tmp0) :
        return len(__tmp0.projects)

    def to_json(__tmp0) -> __typ3:
        return [project.to_json() for project in __tmp0.projects
                if project.name != __tmp0.none_project]


class Config:
    config: ConfigDict

    @staticmethod
    def parse(values: ConfigDict) -> 'Config':
        port = __typ0(values['daemon']['port'])
        host = __typ1(values['daemon']['host'])
        interval = __typ0(values['gui']['interval'])
        run_daemon = __typ2(values['gui']['run_daemon'])
        start_day_time = __typ1(values['gui']['start_day_time'])
        projects = Projects.reinstate(
            values['gui']['projects'],
            __typ1(uuid.uuid4())
        )
        return Config(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp1(__tmp0, port: __typ0, host: __typ1, interval, run_daemon: __typ2,
                 start_day_time, projects: <FILL>) -> None:
        __tmp0.port = port
        __tmp0.host = host
        __tmp0.interval = interval
        __tmp0.run_daemon = run_daemon
        __tmp0.start_day_time = start_day_time
        __tmp0.projects = projects

    def modify(__tmp0, port, host: __typ1, interval, run_daemon: __typ2,
               projects: List[Project]) :
        return Config(port, host, interval, run_daemon, __tmp0.start_day_time,
                      Projects(projects, __tmp0.projects.none_project))

    def get_full_address(__tmp0) :
        return '%s:%s' % (__tmp0.host, __tmp0.port)
