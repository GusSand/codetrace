from typing import TypeAlias
__typ4 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[str, __typ4]


class __typ2:
    APP = 'app'
    WEB = 'web'

    def __tmp6(__tmp0, values) :
        if 'id' in values:
            __tmp0.id = values['id']
            del values['id']
        else:
            __tmp0.id = str(uuid.uuid4())
        __tmp0.values = values

    def to_json(__tmp0) :
        return __tmp0.values

    def __iter__(__tmp0) -> Iterator[Dict[str, str]]:
        return iter(__tmp0.to_json())

    def __getitem__(__tmp0, __tmp1: str) :
        return __tmp0.values[__tmp1]

    def __tmp4(__tmp0, __tmp1: str) -> __typ3:
        return __tmp1 in __tmp0.values

    def __tmp7(__tmp0) -> __typ1:
        return len(__tmp0.values)

    def __tmp3(__tmp0) :
        return __tmp0.values['type'] == __typ2.WEB

    def __tmp2(__tmp0) :
        return __tmp0.values['type'] == __typ2.APP


class Project:
    @staticmethod
    def reinstate(__tmp8: __typ4) :
        return Project(__tmp8['name'],
                       [__typ2(rule) for rule in __tmp8['rules']]
                       )

    @staticmethod
    def create_empty(none_project: str) -> 'Project':
        return Project(none_project, [])

    def __tmp6(__tmp0, name: str, rules) -> None:
        __tmp0.rules = rules
        __tmp0.name = name

    def to_json(__tmp0) -> __typ4:
        return {
            'name': __tmp0.name,
            'rules': [rule.to_json() for rule in __tmp0.rules]
        }


class __typ0:
    @staticmethod
    def reinstate(config_projects: List[__typ4], none_project: str) :
        projects: List['Project'] = []
        for __tmp8 in config_projects:
            rules = [__typ2(rule) for rule in __tmp8['rules']]
            project = Project(__tmp8['name'], rules)
            projects.append(project)

        return __typ0(projects, none_project)

    def __tmp6(__tmp0, projects: List[Project], none_project) -> None:
        __tmp0.none_project = none_project
        __tmp0.projects = projects
        __tmp0.projects.append(Project.create_empty(__tmp0.none_project))

    def __iter__(__tmp0) :
        return iter(__tmp0.projects)

    def __tmp7(__tmp0) -> __typ1:
        return len(__tmp0.projects)

    def to_json(__tmp0) -> __typ4:
        return [project.to_json() for project in __tmp0.projects
                if project.name != __tmp0.none_project]


class Config:
    config: ConfigDict

    @staticmethod
    def parse(values) :
        port = __typ1(values['daemon']['port'])
        host = str(values['daemon']['host'])
        interval = __typ1(values['gui']['interval'])
        run_daemon = __typ3(values['gui']['run_daemon'])
        start_day_time = str(values['gui']['start_day_time'])
        projects = __typ0.reinstate(
            values['gui']['projects'],
            str(uuid.uuid4())
        )
        return Config(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp6(__tmp0, port: __typ1, host, interval: __typ1, run_daemon,
                 start_day_time: <FILL>, projects: __typ0) -> None:
        __tmp0.port = port
        __tmp0.host = host
        __tmp0.interval = interval
        __tmp0.run_daemon = run_daemon
        __tmp0.start_day_time = start_day_time
        __tmp0.projects = projects

    def modify(__tmp0, port: __typ1, host: str, interval, run_daemon: __typ3,
               projects: List[Project]) -> 'Config':
        return Config(port, host, interval, run_daemon, __tmp0.start_day_time,
                      __typ0(projects, __tmp0.projects.none_project))

    def __tmp5(__tmp0) -> str:
        return '%s:%s' % (__tmp0.host, __tmp0.port)
