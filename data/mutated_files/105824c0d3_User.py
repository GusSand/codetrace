from typing import TypeAlias
__typ4 : TypeAlias = "Project"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
__typ3 : TypeAlias = "Audit"
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


def __tmp3(__tmp1, status, __tmp4):
    groupNames = const.StatusByRole.get(__typ1(status), {}).get("group", [])
    users = list(User.objects.filter(group__name__in=groupNames))
    users += [__tmp1]
    actionStr = const.ProjectStatus[__tmp4.status]
    content = messageTpl.format(__tmp1.username, __tmp4.name)
    objs = [
        Message(title=f"{__tmp4.name} {actionStr}通知", content=content, userId=__tmp1.id)
        for __tmp1 in users
    ]
    Message.objects.bulk_create(objs)


class __typ3(object):
    links = getAudits()

    @classmethod
    def next(__tmp2, __tmp1: <FILL>) :
        try:
            index = __tmp2.links.index(__tmp1)
        except ValueError:
            return
        if len(__tmp2.links) < index + 1:
            return
        return __tmp2.links[index + 1]

    @classmethod
    def prev(__tmp2, __tmp1: User) -> User:
        try:
            index = __tmp2.links.index(__tmp1)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return __tmp2.links[index - 1]


class Step(object):
    def __tmp5(__tmp0, step) -> None:
        """
        docstring here
            :param step: Interger
        """
        __tmp0.step = step
        __tmp0.name = projectStatus[step]

    def ok(__tmp0, __tmp1: User) :
        """
        该用户对此状态的项目是否有权限
        """
        return __tmp1.group.name in const.StatusByRole[__typ1(__tmp0.step)]["group"]

    def next(__tmp0, __tmp1, __tmp4: __typ4 = None) :
        step = __tmp0.step
        if __tmp0.name == "审核":
            audit = __typ3.next(__tmp1)
            if audit:
                return __tmp0
        step = __tmp0.step + 1
        if __tmp4:
            __tmp3(__tmp1, step, __tmp4)
        return Step(step)

    def prev(__tmp0, __tmp1: User, __tmp4: __typ4 = None) -> "Step":
        if __tmp0.name == "驳回":
            audit = __typ3.prev(__tmp1)
            if audit:
                return __tmp0
        step = __tmp0.step - 1
        if __tmp4:
            __tmp3(__tmp1, step, __tmp4)
        return Step(step)

    def __call__(__tmp0, __tmp1, action: __typ1, __tmp4: __typ4 = None) -> "Step":
        actionName = const.ProjectLogMapReverse[__typ0(action)]
        if actionName not in projectStatus.values():
            return __tmp0
        if actionName == "驳回":
            return __tmp0.prev(__tmp1, __tmp4)
        return __tmp0.next(__tmp1, __tmp4)

    @classmethod
    def steps(__tmp2, __tmp1) -> typing.List["Step"]:
        """
        @group 用户组
        @role 用户权限
        """
        result = []
        for _step in projectStatus:
            step = __tmp2(_step)
            if step.ok(__tmp1):
                result.append(step)
        return result
