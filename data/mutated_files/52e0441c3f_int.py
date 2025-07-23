from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[__typ1, Any]


class Rule:
    APP = 'app'
    WEB = 'web'

    def __tmp3(__tmp1, values) -> None:
        if 'id' in values:
            __tmp1.id = values['id']
            del values['id']
        else:
            __tmp1.id = __typ1(uuid.uuid4())
        __tmp1.values = values

    def to_json(__tmp1) -> Any:
        return __tmp1.values

    def __tmp4(__tmp1) :
        return iter(__tmp1.to_json())

    def __tmp0(__tmp1, item: __typ1) -> __typ1:
        return __tmp1.values[item]

    def __contains__(__tmp1, item) -> __typ2:
        return item in __tmp1.values

    def __len__(__tmp1) -> int:
        return len(__tmp1.values)

    def __tmp2(__tmp1) :
        return __tmp1.values['type'] == Rule.WEB

    def is_app(__tmp1) -> __typ2:
        return __tmp1.values['type'] == Rule.APP


class Project:
    @staticmethod
    def reinstate(__tmp5: Any) -> 'Project':
        return Project(__tmp5['name'],
                       [Rule(rule) for rule in __tmp5['rules']]
                       )

    @staticmethod
    def create_empty(none_project) -> 'Project':
        return Project(none_project, [])

    def __tmp3(__tmp1, name, rules) -> None:
        __tmp1.rules = rules
        __tmp1.name = name

    def to_json(__tmp1) -> Any:
        return {
            'name': __tmp1.name,
            'rules': [rule.to_json() for rule in __tmp1.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(config_projects: List[Any], none_project: __typ1) :
        projects: List['Project'] = []
        for __tmp5 in config_projects:
            rules = [Rule(rule) for rule in __tmp5['rules']]
            project = Project(__tmp5['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp3(__tmp1, projects: List[Project], none_project: __typ1) :
        __tmp1.none_project = none_project
        __tmp1.projects = projects
        __tmp1.projects.append(Project.create_empty(__tmp1.none_project))

    def __tmp4(__tmp1) -> Iterator[Project]:
        return iter(__tmp1.projects)

    def __len__(__tmp1) -> int:
        return len(__tmp1.projects)

    def to_json(__tmp1) -> Any:
        return [project.to_json() for project in __tmp1.projects
                if project.name != __tmp1.none_project]


class Config:
    config: ConfigDict

    @staticmethod
    def parse(values) -> 'Config':
        port = int(values['daemon']['port'])
        host = __typ1(values['daemon']['host'])
        interval = int(values['gui']['interval'])
        run_daemon = __typ2(values['gui']['run_daemon'])
        start_day_time = __typ1(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            __typ1(uuid.uuid4())
        )
        return Config(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp3(__tmp1, port: <FILL>, host: __typ1, interval: int, run_daemon,
                 start_day_time, projects: __typ0) -> None:
        __tmp1.port = port
        __tmp1.host = host
        __tmp1.interval = interval
        __tmp1.run_daemon = run_daemon
        __tmp1.start_day_time = start_day_time
        __tmp1.projects = projects

    def modify(__tmp1, port: int, host: __typ1, interval: int, run_daemon: __typ2,
               projects: List[Project]) :
        return Config(port, host, interval, run_daemon, __tmp1.start_day_time,
                      __typ0(projects, __tmp1.projects.none_project))

    def get_full_address(__tmp1) :
        return '%s:%s' % (__tmp1.host, __tmp1.port)
