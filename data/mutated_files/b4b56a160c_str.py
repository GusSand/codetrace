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

    def __tmp6(__tmp2, values: Dict[str, str]) :
        if 'id' in values:
            __tmp2.id = values['id']
            del values['id']
        else:
            __tmp2.id = str(uuid.uuid4())
        __tmp2.values = values

    def to_json(__tmp2) -> __typ5:
        return __tmp2.values

    def __tmp5(__tmp2) :
        return iter(__tmp2.to_json())

    def __tmp1(__tmp2, __tmp3: str) :
        return __tmp2.values[__tmp3]

    def __contains__(__tmp2, __tmp3) :
        return __tmp3 in __tmp2.values

    def __tmp7(__tmp2) :
        return len(__tmp2.values)

    def is_web(__tmp2) :
        return __tmp2.values['type'] == __typ3.WEB

    def __tmp4(__tmp2) :
        return __tmp2.values['type'] == __typ3.APP


class __typ6:
    @staticmethod
    def reinstate(__tmp8: __typ5) :
        return __typ6(__tmp8['name'],
                       [__typ3(rule) for rule in __tmp8['rules']]
                       )

    @staticmethod
    def create_empty(none_project) :
        return __typ6(none_project, [])

    def __tmp6(__tmp2, name, rules: List[__typ3]) :
        __tmp2.rules = rules
        __tmp2.name = name

    def to_json(__tmp2) -> __typ5:
        return {
            'name': __tmp2.name,
            'rules': [rule.to_json() for rule in __tmp2.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(__tmp0: List[__typ5], none_project: <FILL>) -> 'Projects':
        projects: List['Project'] = []
        for __tmp8 in __tmp0:
            rules = [__typ3(rule) for rule in __tmp8['rules']]
            project = __typ6(__tmp8['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp6(__tmp2, projects, none_project: str) :
        __tmp2.none_project = none_project
        __tmp2.projects = projects
        __tmp2.projects.append(__typ6.create_empty(__tmp2.none_project))

    def __tmp5(__tmp2) -> Iterator[__typ6]:
        return iter(__tmp2.projects)

    def __tmp7(__tmp2) :
        return len(__tmp2.projects)

    def to_json(__tmp2) :
        return [project.to_json() for project in __tmp2.projects
                if project.name != __tmp2.none_project]


class __typ2:
    config: ConfigDict

    @staticmethod
    def parse(values) -> 'Config':
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

    def __tmp6(__tmp2, port, host: str, interval, run_daemon,
                 start_day_time: str, projects: __typ0) :
        __tmp2.port = port
        __tmp2.host = host
        __tmp2.interval = interval
        __tmp2.run_daemon = run_daemon
        __tmp2.start_day_time = start_day_time
        __tmp2.projects = projects

    def modify(__tmp2, port, host: str, interval: __typ1, run_daemon: __typ4,
               projects) :
        return __typ2(port, host, interval, run_daemon, __tmp2.start_day_time,
                      __typ0(projects, __tmp2.projects.none_project))

    def get_full_address(__tmp2) -> str:
        return '%s:%s' % (__tmp2.host, __tmp2.port)
