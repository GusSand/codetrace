from typing import TypeAlias
__typ3 : TypeAlias = "Audit"
__typ4 : TypeAlias = "User"
__typ2 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
import typing

from ssrd import const

from .models import Config as AuditModel
from .models import Group, Message, Project, User

projectStatus = const.projectStatus


def __tmp0() :
    try:
        obj = AuditModel.objects.first()
        users = [x for x in __typ4.objects.filter(id__in=obj.steps)]
    except Exception:
        users = []
    return users


messageTpl = """尊敬的{}:
    项目{}需要您的处理
"""


def __tmp4(__tmp2, status, __tmp5: <FILL>):
    groupNames = const.StatusByRole.get(__typ2(status), {}).get("group", [])
    users = list(__typ4.objects.filter(group__name__in=groupNames))
    users += [__tmp2]
    actionStr = const.ProjectStatus[__tmp5.status]
    content = messageTpl.format(__tmp2.username, __tmp5.name)
    objs = [
        Message(title=f"{__tmp5.name} {actionStr}通知", content=content, userId=__tmp2.id)
        for __tmp2 in users
    ]
    Message.objects.bulk_create(objs)


class __typ3(object):
    links = __tmp0()

    @classmethod
    def next(__tmp3, __tmp2) :
        try:
            index = __tmp3.links.index(__tmp2)
        except ValueError:
            return
        if len(__tmp3.links) < index + 1:
            return
        return __tmp3.links[index + 1]

    @classmethod
    def prev(__tmp3, __tmp2) :
        try:
            index = __tmp3.links.index(__tmp2)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return __tmp3.links[index - 1]


class __typ1(object):
    def __tmp7(__tmp1, step) :
        """
        docstring here
            :param step: Interger
        """
        __tmp1.step = step
        __tmp1.name = projectStatus[step]

    def ok(__tmp1, __tmp2) :
        """
        该用户对此状态的项目是否有权限
        """
        return __tmp2.group.name in const.StatusByRole[__typ2(__tmp1.step)]["group"]

    def next(__tmp1, __tmp2, __tmp5: Project = None) :
        step = __tmp1.step
        if __tmp1.name == "审核":
            audit = __typ3.next(__tmp2)
            if audit:
                return __tmp1
        step = __tmp1.step + 1
        if __tmp5:
            __tmp4(__tmp2, step, __tmp5)
        return __typ1(step)

    def prev(__tmp1, __tmp2, __tmp5: Project = None) :
        if __tmp1.name == "驳回":
            audit = __typ3.prev(__tmp2)
            if audit:
                return __tmp1
        step = __tmp1.step - 1
        if __tmp5:
            __tmp4(__tmp2, step, __tmp5)
        return __typ1(step)

    def __tmp8(__tmp1, __tmp2, __tmp6, __tmp5: Project = None) :
        actionName = const.ProjectLogMapReverse[__typ0(__tmp6)]
        if actionName not in projectStatus.values():
            return __tmp1
        if actionName == "驳回":
            return __tmp1.prev(__tmp2, __tmp5)
        return __tmp1.next(__tmp2, __tmp5)

    @classmethod
    def steps(__tmp3, __tmp2) :
        """
        @group 用户组
        @role 用户权限
        """
        result = []
        for _step in projectStatus:
            step = __tmp3(_step)
            if step.ok(__tmp2):
                result.append(step)
        return result
