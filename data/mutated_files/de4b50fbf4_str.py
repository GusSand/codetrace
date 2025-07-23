from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
import uuid
from typing import Dict, Any, List, Iterator

ConfigDict = Dict[str, Any]


class Rule:
    APP = 'app'
    WEB = 'web'

    def __tmp6(__tmp1, values) :
        if 'id' in values:
            __tmp1.id = values['id']
            del values['id']
        else:
            __tmp1.id = str(uuid.uuid4())
        __tmp1.values = values

    def to_json(__tmp1) :
        return __tmp1.values

    def __iter__(__tmp1) -> Iterator[Dict[str, str]]:
        return iter(__tmp1.to_json())

    def __tmp0(__tmp1, __tmp2) :
        return __tmp1.values[__tmp2]

    def __tmp4(__tmp1, __tmp2) :
        return __tmp2 in __tmp1.values

    def __tmp8(__tmp1) :
        return len(__tmp1.values)

    def __tmp5(__tmp1) :
        return __tmp1.values['type'] == Rule.WEB

    def __tmp3(__tmp1) -> __typ2:
        return __tmp1.values['type'] == Rule.APP


class Project:
    @staticmethod
    def reinstate(config_project) :
        return Project(config_project['name'],
                       [Rule(rule) for rule in config_project['rules']]
                       )

    @staticmethod
    def create_empty(none_project: str) -> 'Project':
        return Project(none_project, [])

    def __tmp6(__tmp1, name: <FILL>, rules: List[Rule]) -> None:
        __tmp1.rules = rules
        __tmp1.name = name

    def to_json(__tmp1) :
        return {
            'name': __tmp1.name,
            'rules': [rule.to_json() for rule in __tmp1.rules]
        }


class Projects:
    @staticmethod
    def reinstate(config_projects, none_project) :
        projects: List['Project'] = []
        for config_project in config_projects:
            rules = [Rule(rule) for rule in config_project['rules']]
            project = Project(config_project['name'], rules)
            projects.append(project)

        return Projects(projects, none_project)

    def __tmp6(__tmp1, projects: List[Project], none_project: str) :
        __tmp1.none_project = none_project
        __tmp1.projects = projects
        __tmp1.projects.append(Project.create_empty(__tmp1.none_project))

    def __iter__(__tmp1) :
        return iter(__tmp1.projects)

    def __tmp8(__tmp1) -> __typ0:
        return len(__tmp1.projects)

    def to_json(__tmp1) -> Any:
        return [project.to_json() for project in __tmp1.projects
                if project.name != __tmp1.none_project]


class __typ1:
    config: ConfigDict

    @staticmethod
    def __tmp9(values: ConfigDict) :
        port = __typ0(values['daemon']['port'])
        host = str(values['daemon']['host'])
        interval = __typ0(values['gui']['interval'])
        run_daemon = __typ2(values['gui']['run_daemon'])
        start_day_time = str(values['gui']['start_day_time'])
        projects = Projects.reinstate(
            values['gui']['projects'],
            str(uuid.uuid4())
        )
        return __typ1(port, host, interval, run_daemon, start_day_time,
                      projects)

    def __tmp6(__tmp1, port, host, interval, run_daemon,
                 start_day_time: str, projects) -> None:
        __tmp1.port = port
        __tmp1.host = host
        __tmp1.interval = interval
        __tmp1.run_daemon = run_daemon
        __tmp1.start_day_time = start_day_time
        __tmp1.projects = projects

    def __tmp7(__tmp1, port, host: str, interval: __typ0, run_daemon,
               projects: List[Project]) -> 'Config':
        return __typ1(port, host, interval, run_daemon, __tmp1.start_day_time,
                      Projects(projects, __tmp1.projects.none_project))

    def get_full_address(__tmp1) -> str:
        return '%s:%s' % (__tmp1.host, __tmp1.port)
