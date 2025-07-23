from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ5 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[str, __typ5]


class __typ3:
    APP = 'app'
    WEB = 'web'

    def __tmp6(__tmp0, values: Dict[str, str]) -> None:
        if 'id' in values:
            __tmp0.id = values['id']
            del values['id']
        else:
            __tmp0.id = str(uuid.uuid4())
        __tmp0.values = values

    def to_json(__tmp0) -> __typ5:
        return __tmp0.values

    def __tmp5(__tmp0) -> Iterator[Dict[str, str]]:
        return iter(__tmp0.to_json())

    def __getitem__(__tmp0, __tmp1: <FILL>) :
        return __tmp0.values[__tmp1]

    def __tmp2(__tmp0, __tmp1: str) -> __typ4:
        return __tmp1 in __tmp0.values

    def __tmp8(__tmp0) :
        return len(__tmp0.values)

    def is_web(__tmp0) -> __typ4:
        return __tmp0.values['type'] == __typ3.WEB

    def __tmp3(__tmp0) :
        return __tmp0.values['type'] == __typ3.APP


class __typ6:
    @staticmethod
    def reinstate(__tmp9) -> 'Project':
        return __typ6(__tmp9['name'],
                       [__typ3(rule) for rule in __tmp9['rules']]
                       )

    @staticmethod
    def create_empty(none_project: str) -> 'Project':
        return __typ6(none_project, [])

    def __tmp6(__tmp0, name: str, rules: List[__typ3]) :
        __tmp0.rules = rules
        __tmp0.name = name

    def to_json(__tmp0) -> __typ5:
        return {
            'name': __tmp0.name,
            'rules': [rule.to_json() for rule in __tmp0.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(config_projects, none_project: str) :
        projects: List['Project'] = []
        for __tmp9 in config_projects:
            rules = [__typ3(rule) for rule in __tmp9['rules']]
            project = __typ6(__tmp9['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp6(__tmp0, projects: List[__typ6], none_project) :
        __tmp0.none_project = none_project
        __tmp0.projects = projects
        __tmp0.projects.append(__typ6.create_empty(__tmp0.none_project))

    def __tmp5(__tmp0) :
        return iter(__tmp0.projects)

    def __tmp8(__tmp0) -> __typ1:
        return len(__tmp0.projects)

    def to_json(__tmp0) -> __typ5:
        return [project.to_json() for project in __tmp0.projects
                if project.name != __tmp0.none_project]


class __typ2:
    config: ConfigDict

    @staticmethod
    def __tmp10(values: ConfigDict) :
        port = __typ1(values['daemon']['port'])
        host = str(values['daemon']['host'])
        interval = __typ1(values['gui']['interval'])
        run_daemon = __typ4(values['gui']['run_daemon'])
        start_day_time = str(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            str(uuid.uuid4())
        )
        return __typ2(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp6(__tmp0, port: __typ1, host: str, interval: __typ1, run_daemon,
                 start_day_time, projects: __typ0) -> None:
        __tmp0.port = port
        __tmp0.host = host
        __tmp0.interval = interval
        __tmp0.run_daemon = run_daemon
        __tmp0.start_day_time = start_day_time
        __tmp0.projects = projects

    def __tmp7(__tmp0, port: __typ1, host, interval: __typ1, run_daemon: __typ4,
               projects) -> 'Config':
        return __typ2(port, host, interval, run_daemon, __tmp0.start_day_time,
                      __typ0(projects, __tmp0.projects.none_project))

    def __tmp4(__tmp0) -> str:
        return '%s:%s' % (__tmp0.host, __tmp0.port)
