from typing import TypeAlias
__typ5 : TypeAlias = "bool"
__typ6 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

__typ4 = Dict[str, __typ6]


class __typ2:
    APP = 'app'
    WEB = 'web'

    def __init__(__tmp0, values: Dict[str, str]) -> None:
        if 'id' in values:
            __tmp0.id = values['id']
            del values['id']
        else:
            __tmp0.id = str(uuid.uuid4())
        __tmp0.values = values

    def to_json(__tmp0) -> __typ6:
        return __tmp0.values

    def __iter__(__tmp0) -> Iterator[Dict[str, str]]:
        return iter(__tmp0.to_json())

    def __getitem__(__tmp0, item: str) -> str:
        return __tmp0.values[item]

    def __contains__(__tmp0, item: str) :
        return item in __tmp0.values

    def __len__(__tmp0) -> __typ1:
        return len(__tmp0.values)

    def is_web(__tmp0) -> __typ5:
        return __tmp0.values['type'] == __typ2.WEB

    def is_app(__tmp0) -> __typ5:
        return __tmp0.values['type'] == __typ2.APP


class __typ7:
    @staticmethod
    def reinstate(config_project: __typ6) -> 'Project':
        return __typ7(config_project['name'],
                       [__typ2(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project: <FILL>) :
        return __typ7(none_project, [])

    def __init__(__tmp0, name: str, rules: List[__typ2]) -> None:
        __tmp0.rules = rules
        __tmp0.name = name

    def to_json(__tmp0) -> __typ6:
        return {
            'name': __tmp0.name,
            'rules': [rule.to_json() for rule in __tmp0.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(config_projects: List[__typ6], none_project: str) -> 'Projects':
        projects: List['Project'] = []
        for config_project in config_projects:
            rules = [__typ2(rule) for rule in config_project['rules']]
            project = __typ7(config_project['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __init__(__tmp0, projects: List[__typ7], none_project: str) -> None:
        __tmp0.none_project = none_project
        __tmp0.projects = projects
        __tmp0.projects.append(__typ7.create_empty(__tmp0.none_project))

    def __iter__(__tmp0) -> Iterator[__typ7]:
        return iter(__tmp0.projects)

    def __len__(__tmp0) -> __typ1:
        return len(__tmp0.projects)

    def to_json(__tmp0) -> __typ6:
        return [project.to_json() for project in __tmp0.projects
                if project.name != __tmp0.none_project]


class __typ3:
    config: __typ4

    @staticmethod
    def parse(values) -> 'Config':
        port = __typ1(values['daemon']['port'])
        host = str(values['daemon']['host'])
        interval = __typ1(values['gui']['interval'])
        run_daemon = __typ5(values['gui']['run_daemon'])
        start_day_time = str(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            str(uuid.uuid4())
        )
        return __typ3(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __init__(__tmp0, port: __typ1, host, interval, run_daemon,
                 start_day_time: str, projects: __typ0) -> None:
        __tmp0.port = port
        __tmp0.host = host
        __tmp0.interval = interval
        __tmp0.run_daemon = run_daemon
        __tmp0.start_day_time = start_day_time
        __tmp0.projects = projects

    def modify(__tmp0, port: __typ1, host: str, interval: __typ1, run_daemon: __typ5,
               projects: List[__typ7]) -> 'Config':
        return __typ3(port, host, interval, run_daemon, __tmp0.start_day_time,
                      __typ0(projects, __tmp0.projects.none_project))

    def get_full_address(__tmp0) -> str:
        return '%s:%s' % (__tmp0.host, __tmp0.port)
