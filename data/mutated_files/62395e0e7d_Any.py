from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

__typ3 = Dict[__typ2, Any]


class Rule:
    APP = 'app'
    WEB = 'web'

    def __tmp3(__tmp1, values: Dict[__typ2, __typ2]) :
        if 'id' in values:
            __tmp1.id = values['id']
            del values['id']
        else:
            __tmp1.id = __typ2(uuid.uuid4())
        __tmp1.values = values

    def to_json(__tmp1) -> Any:
        return __tmp1.values

    def __tmp4(__tmp1) -> Iterator[Dict[__typ2, __typ2]]:
        return iter(__tmp1.to_json())

    def __tmp0(__tmp1, item: __typ2) -> __typ2:
        return __tmp1.values[item]

    def __contains__(__tmp1, item: __typ2) -> bool:
        return item in __tmp1.values

    def __tmp6(__tmp1) -> __typ1:
        return len(__tmp1.values)

    def is_web(__tmp1) -> bool:
        return __tmp1.values['type'] == Rule.WEB

    def is_app(__tmp1) :
        return __tmp1.values['type'] == Rule.APP


class Project:
    @staticmethod
    def reinstate(config_project: <FILL>) -> 'Project':
        return Project(config_project['name'],
                       [Rule(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project: __typ2) -> 'Project':
        return Project(none_project, [])

    def __tmp3(__tmp1, name: __typ2, rules: List[Rule]) -> None:
        __tmp1.rules = rules
        __tmp1.name = name

    def to_json(__tmp1) :
        return {
            'name': __tmp1.name,
            'rules': [rule.to_json() for rule in __tmp1.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(config_projects: List[Any], none_project: __typ2) :
        projects: List['Project'] = []
        for config_project in config_projects:
            rules = [Rule(rule) for rule in config_project['rules']]
            project = Project(config_project['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp3(__tmp1, projects: List[Project], none_project: __typ2) :
        __tmp1.none_project = none_project
        __tmp1.projects = projects
        __tmp1.projects.append(Project.create_empty(__tmp1.none_project))

    def __tmp4(__tmp1) -> Iterator[Project]:
        return iter(__tmp1.projects)

    def __tmp6(__tmp1) -> __typ1:
        return len(__tmp1.projects)

    def to_json(__tmp1) -> Any:
        return [project.to_json() for project in __tmp1.projects
                if project.name != __tmp1.none_project]


class Config:
    config: __typ3

    @staticmethod
    def __tmp7(values: __typ3) :
        port = __typ1(values['daemon']['port'])
        host = __typ2(values['daemon']['host'])
        interval = __typ1(values['gui']['interval'])
        run_daemon = bool(values['gui']['run_daemon'])
        start_day_time = __typ2(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            __typ2(uuid.uuid4())
        )
        return Config(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp3(__tmp1, port: __typ1, host: __typ2, interval: __typ1, run_daemon: bool,
                 start_day_time: __typ2, projects: __typ0) -> None:
        __tmp1.port = port
        __tmp1.host = host
        __tmp1.interval = interval
        __tmp1.run_daemon = run_daemon
        __tmp1.start_day_time = start_day_time
        __tmp1.projects = projects

    def __tmp5(__tmp1, port: __typ1, host: __typ2, interval, run_daemon: bool,
               projects: List[Project]) -> 'Config':
        return Config(port, host, interval, run_daemon, __tmp1.start_day_time,
                      __typ0(projects, __tmp1.projects.none_project))

    def __tmp2(__tmp1) -> __typ2:
        return '%s:%s' % (__tmp1.host, __tmp1.port)
