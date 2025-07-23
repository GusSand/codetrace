from typing import TypeAlias
__typ1 : TypeAlias = "Audit"
__typ0 : TypeAlias = "int"
import typing

from ssrd import const

from .models import Config as AuditModel
from .models import Group, Message, Project, User

projectStatus = const.projectStatus


def getAudits() -> typing.List[User]:
    try:
        obj = AuditModel.objects.first()
        users = [x for x in User.objects.filter(id__in=obj.steps)]
    except Exception:
        users = []
    return users


messageTpl = """尊敬的{}:
    项目{}需要您的处理
"""


def createMessage(__tmp0: User, status: __typ0, project: Project):
    groupNames = const.StatusByRole.get(str(status), {}).get("group", [])
    users = list(User.objects.filter(group__name__in=groupNames))
    users += [__tmp0]
    actionStr = const.ProjectStatus[project.status]
    content = messageTpl.format(__tmp0.username, project.name)
    objs = [
        Message(title=f"{project.name} {actionStr}通知", content=content, userId=__tmp0.id)
        for __tmp0 in users
    ]
    Message.objects.bulk_create(objs)


class __typ1(object):
    links = getAudits()

    @classmethod
    def next(cls, __tmp0) :
        try:
            index = cls.links.index(__tmp0)
        except ValueError:
            return
        if len(cls.links) < index + 1:
            return
        return cls.links[index + 1]

    @classmethod
    def prev(cls, __tmp0: <FILL>) -> User:
        try:
            index = cls.links.index(__tmp0)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return cls.links[index - 1]


class Step(object):
    def __init__(self, step) :
        """
        docstring here
            :param step: Interger
        """
        self.step = step
        self.name = projectStatus[step]

    def ok(self, __tmp0: User) :
        """
        该用户对此状态的项目是否有权限
        """
        return __tmp0.group.name in const.StatusByRole[str(self.step)]["group"]

    def next(self, __tmp0, project: Project = None) -> "Step":
        step = self.step
        if self.name == "审核":
            audit = __typ1.next(__tmp0)
            if audit:
                return self
        step = self.step + 1
        if project:
            createMessage(__tmp0, step, project)
        return Step(step)

    def prev(self, __tmp0, project: Project = None) :
        if self.name == "驳回":
            audit = __typ1.prev(__tmp0)
            if audit:
                return self
        step = self.step - 1
        if project:
            createMessage(__tmp0, step, project)
        return Step(step)

    def __call__(self, __tmp0, action, project: Project = None) :
        actionName = const.ProjectLogMapReverse[__typ0(action)]
        if actionName not in projectStatus.values():
            return self
        if actionName == "驳回":
            return self.prev(__tmp0, project)
        return self.next(__tmp0, project)

    @classmethod
    def steps(cls, __tmp0) :
        """
        @group 用户组
        @role 用户权限
        """
        result = []
        for _step in projectStatus:
            step = cls(_step)
            if step.ok(__tmp0):
                result.append(step)
        return result
