from typing import TypeAlias
__typ5 : TypeAlias = "Project"
__typ0 : TypeAlias = "int"
__typ4 : TypeAlias = "Audit"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"
import typing

from ssrd import const

from .models import Config as AuditModel
from .models import Group, Message, Project, User

projectStatus = const.projectStatus


def getAudits() :
    try:
        obj = AuditModel.objects.first()
        users = [x for x in User.objects.filter(id__in=obj.steps)]
    except Exception:
        users = []
    return users


messageTpl = """尊敬的{}:
    项目{}需要您的处理
"""


def __tmp0(__tmp3: User, status: __typ0, project):
    groupNames = const.StatusByRole.get(__typ2(status), {}).get("group", [])
    users = list(User.objects.filter(group__name__in=groupNames))
    users += [__tmp3]
    actionStr = const.ProjectStatus[project.status]
    content = messageTpl.format(__tmp3.username, project.name)
    objs = [
        Message(title=f"{project.name} {actionStr}通知", content=content, userId=__tmp3.id)
        for __tmp3 in users
    ]
    Message.objects.bulk_create(objs)


class __typ4(object):
    links = getAudits()

    @classmethod
    def next(cls, __tmp3: User) :
        try:
            index = cls.links.index(__tmp3)
        except ValueError:
            return
        if len(cls.links) < index + 1:
            return
        return cls.links[index + 1]

    @classmethod
    def prev(cls, __tmp3: User) -> User:
        try:
            index = cls.links.index(__tmp3)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return cls.links[index - 1]


class __typ1(object):
    def __tmp1(__tmp2, step) :
        """
        docstring here
            :param step: Interger
        """
        __tmp2.step = step
        __tmp2.name = projectStatus[step]

    def ok(__tmp2, __tmp3) -> __typ3:
        """
        该用户对此状态的项目是否有权限
        """
        return __tmp3.group.name in const.StatusByRole[__typ2(__tmp2.step)]["group"]

    def next(__tmp2, __tmp3: User, project: __typ5 = None) :
        step = __tmp2.step
        if __tmp2.name == "审核":
            audit = __typ4.next(__tmp3)
            if audit:
                return __tmp2
        step = __tmp2.step + 1
        if project:
            __tmp0(__tmp3, step, project)
        return __typ1(step)

    def prev(__tmp2, __tmp3, project: __typ5 = None) :
        if __tmp2.name == "驳回":
            audit = __typ4.prev(__tmp3)
            if audit:
                return __tmp2
        step = __tmp2.step - 1
        if project:
            __tmp0(__tmp3, step, project)
        return __typ1(step)

    def __call__(__tmp2, __tmp3: <FILL>, action: __typ2, project: __typ5 = None) -> "Step":
        actionName = const.ProjectLogMapReverse[__typ0(action)]
        if actionName not in projectStatus.values():
            return __tmp2
        if actionName == "驳回":
            return __tmp2.prev(__tmp3, project)
        return __tmp2.next(__tmp3, project)

    @classmethod
    def steps(cls, __tmp3: User) -> typing.List["Step"]:
        """
        @group 用户组
        @role 用户权限
        """
        result = []
        for _step in projectStatus:
            step = cls(_step)
            if step.ok(__tmp3):
                result.append(step)
        return result
