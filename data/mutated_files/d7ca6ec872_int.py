from typing import TypeAlias
__typ5 : TypeAlias = "bool"
__typ6 : TypeAlias = "Any"
__typ4 : TypeAlias = "str"
import uuid
from typing import Dict, Any, List, Iterator

__typ3 = Dict[__typ4, __typ6]


class __typ1:
    APP = 'app'
    WEB = 'web'

    def __tmp5(__tmp0, values) :
        if 'id' in values:
            __tmp0.id = values['id']
            del values['id']
        else:
            __tmp0.id = __typ4(uuid.uuid4())
        __tmp0.values = values

    def to_json(__tmp0) :
        return __tmp0.values

    def __tmp6(__tmp0) -> Iterator[Dict[__typ4, __typ4]]:
        return iter(__tmp0.to_json())

    def __getitem__(__tmp0, __tmp1) -> __typ4:
        return __tmp0.values[__tmp1]

    def __tmp2(__tmp0, __tmp1: __typ4) -> __typ5:
        return __tmp1 in __tmp0.values

    def __tmp8(__tmp0) :
        return len(__tmp0.values)

    def __tmp3(__tmp0) :
        return __tmp0.values['type'] == __typ1.WEB

    def is_app(__tmp0) :
        return __tmp0.values['type'] == __typ1.APP


class __typ7:
    @staticmethod
    def reinstate(config_project) :
        return __typ7(config_project['name'],
                       [__typ1(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project) :
        return __typ7(none_project, [])

    def __tmp5(__tmp0, name, rules: List[__typ1]) :
        __tmp0.rules = rules
        __tmp0.name = name

    def to_json(__tmp0) :
        return {
            'name': __tmp0.name,
            'rules': [rule.to_json() for rule in __tmp0.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(config_projects, none_project) :
        projects: List['Project'] = []
        for config_project in config_projects:
            rules = [__typ1(rule) for rule in config_project['rules']]
            project = __typ7(config_project['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp5(__tmp0, projects, none_project) :
        __tmp0.none_project = none_project
        __tmp0.projects = projects
        __tmp0.projects.append(__typ7.create_empty(__tmp0.none_project))

    def __tmp6(__tmp0) :
        return iter(__tmp0.projects)

    def __tmp8(__tmp0) :
        return len(__tmp0.projects)

    def to_json(__tmp0) :
        return [project.to_json() for project in __tmp0.projects
                if project.name != __tmp0.none_project]


class __typ2:
    config: __typ3

    @staticmethod
    def parse(values) :
        port = int(values['daemon']['port'])
        host = __typ4(values['daemon']['host'])
        interval = int(values['gui']['interval'])
        run_daemon = __typ5(values['gui']['run_daemon'])
        start_day_time = __typ4(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            __typ4(uuid.uuid4())
        )
        return __typ2(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp5(__tmp0, port, host, interval: <FILL>, run_daemon,
                 start_day_time, projects) :
        __tmp0.port = port
        __tmp0.host = host
        __tmp0.interval = interval
        __tmp0.run_daemon = run_daemon
        __tmp0.start_day_time = start_day_time
        __tmp0.projects = projects

    def __tmp7(__tmp0, port: int, host, interval: int, run_daemon: __typ5,
               projects: List[__typ7]) -> 'Config':
        return __typ2(port, host, interval, run_daemon, __tmp0.start_day_time,
                      __typ0(projects, __tmp0.projects.none_project))

    def __tmp4(__tmp0) :
        return '%s:%s' % (__tmp0.host, __tmp0.port)
