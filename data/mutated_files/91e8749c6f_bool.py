from typing import TypeAlias
__typ4 : TypeAlias = "str"
__typ5 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[__typ4, __typ5]


class __typ3:
    APP = 'app'
    WEB = 'web'

    def __tmp5(__tmp1, values: Dict[__typ4, __typ4]) :
        if 'id' in values:
            __tmp1.id = values['id']
            del values['id']
        else:
            __tmp1.id = __typ4(uuid.uuid4())
        __tmp1.values = values

    def to_json(__tmp1) -> __typ5:
        return __tmp1.values

    def __tmp4(__tmp1) -> Iterator[Dict[__typ4, __typ4]]:
        return iter(__tmp1.to_json())

    def __getitem__(__tmp1, __tmp2: __typ4) :
        return __tmp1.values[__tmp2]

    def __tmp3(__tmp1, __tmp2: __typ4) -> bool:
        return __tmp2 in __tmp1.values

    def __tmp6(__tmp1) -> __typ1:
        return len(__tmp1.values)

    def is_web(__tmp1) -> bool:
        return __tmp1.values['type'] == __typ3.WEB

    def is_app(__tmp1) -> bool:
        return __tmp1.values['type'] == __typ3.APP


class __typ6:
    @staticmethod
    def reinstate(config_project: __typ5) -> 'Project':
        return __typ6(config_project['name'],
                       [__typ3(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project: __typ4) -> 'Project':
        return __typ6(none_project, [])

    def __tmp5(__tmp1, name: __typ4, rules: List[__typ3]) -> None:
        __tmp1.rules = rules
        __tmp1.name = name

    def to_json(__tmp1) -> __typ5:
        return {
            'name': __tmp1.name,
            'rules': [rule.to_json() for rule in __tmp1.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(__tmp0: List[__typ5], none_project: __typ4) -> 'Projects':
        projects: List['Project'] = []
        for config_project in __tmp0:
            rules = [__typ3(rule) for rule in config_project['rules']]
            project = __typ6(config_project['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp5(__tmp1, projects: List[__typ6], none_project: __typ4) -> None:
        __tmp1.none_project = none_project
        __tmp1.projects = projects
        __tmp1.projects.append(__typ6.create_empty(__tmp1.none_project))

    def __tmp4(__tmp1) -> Iterator[__typ6]:
        return iter(__tmp1.projects)

    def __tmp6(__tmp1) -> __typ1:
        return len(__tmp1.projects)

    def to_json(__tmp1) -> __typ5:
        return [project.to_json() for project in __tmp1.projects
                if project.name != __tmp1.none_project]


class __typ2:
    config: ConfigDict

    @staticmethod
    def parse(values: ConfigDict) -> 'Config':
        port = __typ1(values['daemon']['port'])
        host = __typ4(values['daemon']['host'])
        interval = __typ1(values['gui']['interval'])
        run_daemon = bool(values['gui']['run_daemon'])
        start_day_time = __typ4(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            __typ4(uuid.uuid4())
        )
        return __typ2(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp5(__tmp1, port, host: __typ4, interval: __typ1, run_daemon: bool,
                 start_day_time: __typ4, projects: __typ0) -> None:
        __tmp1.port = port
        __tmp1.host = host
        __tmp1.interval = interval
        __tmp1.run_daemon = run_daemon
        __tmp1.start_day_time = start_day_time
        __tmp1.projects = projects

    def modify(__tmp1, port: __typ1, host: __typ4, interval: __typ1, run_daemon: <FILL>,
               projects: List[__typ6]) -> 'Config':
        return __typ2(port, host, interval, run_daemon, __tmp1.start_day_time,
                      __typ0(projects, __tmp1.projects.none_project))

    def get_full_address(__tmp1) -> __typ4:
        return '%s:%s' % (__tmp1.host, __tmp1.port)
