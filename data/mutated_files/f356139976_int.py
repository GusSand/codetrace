from typing import TypeAlias
__typ3 : TypeAlias = "str"
__typ4 : TypeAlias = "bool"
__typ5 : TypeAlias = "Any"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[__typ3, __typ5]


class __typ1:
    APP = 'app'
    WEB = 'web'

    def __tmp6(__tmp2, values: Dict[__typ3, __typ3]) :
        if 'id' in values:
            __tmp2.id = values['id']
            del values['id']
        else:
            __tmp2.id = __typ3(uuid.uuid4())
        __tmp2.values = values

    def to_json(__tmp2) -> __typ5:
        return __tmp2.values

    def __tmp8(__tmp2) :
        return iter(__tmp2.to_json())

    def __tmp1(__tmp2, item: __typ3) :
        return __tmp2.values[item]

    def __contains__(__tmp2, item) :
        return item in __tmp2.values

    def __tmp9(__tmp2) -> int:
        return len(__tmp2.values)

    def __tmp4(__tmp2) :
        return __tmp2.values['type'] == __typ1.WEB

    def __tmp3(__tmp2) :
        return __tmp2.values['type'] == __typ1.APP


class __typ6:
    @staticmethod
    def reinstate(config_project) :
        return __typ6(config_project['name'],
                       [__typ1(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project) :
        return __typ6(none_project, [])

    def __tmp6(__tmp2, name, rules) :
        __tmp2.rules = rules
        __tmp2.name = name

    def to_json(__tmp2) :
        return {
            'name': __tmp2.name,
            'rules': [rule.to_json() for rule in __tmp2.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(__tmp0, none_project) :
        projects: List['Project'] = []
        for config_project in __tmp0:
            rules = [__typ1(rule) for rule in config_project['rules']]
            project = __typ6(config_project['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp6(__tmp2, projects, none_project) :
        __tmp2.none_project = none_project
        __tmp2.projects = projects
        __tmp2.projects.append(__typ6.create_empty(__tmp2.none_project))

    def __tmp8(__tmp2) :
        return iter(__tmp2.projects)

    def __tmp9(__tmp2) :
        return len(__tmp2.projects)

    def to_json(__tmp2) :
        return [project.to_json() for project in __tmp2.projects
                if project.name != __tmp2.none_project]


class __typ2:
    config: ConfigDict

    @staticmethod
    def parse(values) :
        port = int(values['daemon']['port'])
        host = __typ3(values['daemon']['host'])
        interval = int(values['gui']['interval'])
        run_daemon = __typ4(values['gui']['run_daemon'])
        start_day_time = __typ3(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            __typ3(uuid.uuid4())
        )
        return __typ2(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp6(__tmp2, port, host, interval, run_daemon,
                 start_day_time, projects) :
        __tmp2.port = port
        __tmp2.host = host
        __tmp2.interval = interval
        __tmp2.run_daemon = run_daemon
        __tmp2.start_day_time = start_day_time
        __tmp2.projects = projects

    def __tmp7(__tmp2, port, host, interval: <FILL>, run_daemon,
               projects) :
        return __typ2(port, host, interval, run_daemon, __tmp2.start_day_time,
                      __typ0(projects, __tmp2.projects.none_project))

    def __tmp5(__tmp2) :
        return '%s:%s' % (__tmp2.host, __tmp2.port)
