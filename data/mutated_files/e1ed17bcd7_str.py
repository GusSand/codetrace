from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ5 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[str, __typ5]


class __typ2:
    APP = 'app'
    WEB = 'web'

    def __init__(__tmp1, values) -> None:
        if 'id' in values:
            __tmp1.id = values['id']
            del values['id']
        else:
            __tmp1.id = str(uuid.uuid4())
        __tmp1.values = values

    def to_json(__tmp1) -> __typ5:
        return __tmp1.values

    def __tmp5(__tmp1) -> Iterator[Dict[str, str]]:
        return iter(__tmp1.to_json())

    def __getitem__(__tmp1, __tmp2: str) -> str:
        return __tmp1.values[__tmp2]

    def __contains__(__tmp1, __tmp2: str) -> __typ4:
        return __tmp2 in __tmp1.values

    def __len__(__tmp1) -> __typ1:
        return len(__tmp1.values)

    def __tmp3(__tmp1) -> __typ4:
        return __tmp1.values['type'] == __typ2.WEB

    def is_app(__tmp1) -> __typ4:
        return __tmp1.values['type'] == __typ2.APP


class Project:
    @staticmethod
    def reinstate(config_project) -> 'Project':
        return Project(config_project['name'],
                       [__typ2(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project) :
        return Project(none_project, [])

    def __init__(__tmp1, name: str, rules) :
        __tmp1.rules = rules
        __tmp1.name = name

    def to_json(__tmp1) :
        return {
            'name': __tmp1.name,
            'rules': [rule.to_json() for rule in __tmp1.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(__tmp0: List[__typ5], none_project: str) -> 'Projects':
        projects: List['Project'] = []
        for config_project in __tmp0:
            rules = [__typ2(rule) for rule in config_project['rules']]
            project = Project(config_project['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __init__(__tmp1, projects: List[Project], none_project: str) -> None:
        __tmp1.none_project = none_project
        __tmp1.projects = projects
        __tmp1.projects.append(Project.create_empty(__tmp1.none_project))

    def __tmp5(__tmp1) -> Iterator[Project]:
        return iter(__tmp1.projects)

    def __len__(__tmp1) -> __typ1:
        return len(__tmp1.projects)

    def to_json(__tmp1) -> __typ5:
        return [project.to_json() for project in __tmp1.projects
                if project.name != __tmp1.none_project]


class __typ3:
    config: ConfigDict

    @staticmethod
    def __tmp6(values: ConfigDict) -> 'Config':
        port = __typ1(values['daemon']['port'])
        host = str(values['daemon']['host'])
        interval = __typ1(values['gui']['interval'])
        run_daemon = __typ4(values['gui']['run_daemon'])
        start_day_time = str(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            str(uuid.uuid4())
        )
        return __typ3(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __init__(__tmp1, port: __typ1, host: <FILL>, interval, run_daemon: __typ4,
                 start_day_time: str, projects: __typ0) :
        __tmp1.port = port
        __tmp1.host = host
        __tmp1.interval = interval
        __tmp1.run_daemon = run_daemon
        __tmp1.start_day_time = start_day_time
        __tmp1.projects = projects

    def modify(__tmp1, port: __typ1, host: str, interval: __typ1, run_daemon: __typ4,
               projects: List[Project]) -> 'Config':
        return __typ3(port, host, interval, run_daemon, __tmp1.start_day_time,
                      __typ0(projects, __tmp1.projects.none_project))

    def __tmp4(__tmp1) -> str:
        return '%s:%s' % (__tmp1.host, __tmp1.port)
