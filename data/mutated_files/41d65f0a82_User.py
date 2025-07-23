from typing import TypeAlias
__typ1 : TypeAlias = "Audit"
__typ0 : TypeAlias = "int"
import typing

from ssrd import const

from .models import Config as AuditModel
from .models import Group, Message, Project, User

projectStatus = const.projectStatus


def __tmp0() -> typing.List[User]:
    try:
        obj = AuditModel.objects.first()
        users = [x for x in User.objects.filter(id__in=obj.steps)]
    except Exception:
        users = []
    return users


messageTpl = """尊敬的{}:
    项目{}需要您的处理
"""


def createMessage(__tmp2: User, status: __typ0, __tmp4: Project):
    groupNames = const.StatusByRole.get(str(status), {}).get("group", [])
    users = list(User.objects.filter(group__name__in=groupNames))
    users += [__tmp2]
    actionStr = const.ProjectStatus[__tmp4.status]
    content = messageTpl.format(__tmp2.username, __tmp4.name)
    objs = [
        Message(title=f"{__tmp4.name} {actionStr}通知", content=content, userId=__tmp2.id)
        for __tmp2 in users
    ]
    Message.objects.bulk_create(objs)


class __typ1(object):
    links = __tmp0()

    @classmethod
    def next(__tmp3, __tmp2: User) -> User:
        try:
            index = __tmp3.links.index(__tmp2)
        except ValueError:
            return
        if len(__tmp3.links) < index + 1:
            return
        return __tmp3.links[index + 1]

    @classmethod
    def prev(__tmp3, __tmp2: User) :
        try:
            index = __tmp3.links.index(__tmp2)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return __tmp3.links[index - 1]


class __typ2(object):
    def __tmp5(__tmp1, step) -> None:
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
        return __tmp2.group.name in const.StatusByRole[str(__tmp1.step)]["group"]

    def next(__tmp1, __tmp2: <FILL>, __tmp4: Project = None) -> "Step":
        step = __tmp1.step
        if __tmp1.name == "审核":
            audit = __typ1.next(__tmp2)
            if audit:
                return __tmp1
        step = __tmp1.step + 1
        if __tmp4:
            createMessage(__tmp2, step, __tmp4)
        return __typ2(step)

    def prev(__tmp1, __tmp2: User, __tmp4: Project = None) :
        if __tmp1.name == "驳回":
            audit = __typ1.prev(__tmp2)
            if audit:
                return __tmp1
        step = __tmp1.step - 1
        if __tmp4:
            createMessage(__tmp2, step, __tmp4)
        return __typ2(step)

    def __tmp6(__tmp1, __tmp2: User, action: str, __tmp4: Project = None) -> "Step":
        actionName = const.ProjectLogMapReverse[__typ0(action)]
        if actionName not in projectStatus.values():
            return __tmp1
        if actionName == "驳回":
            return __tmp1.prev(__tmp2, __tmp4)
        return __tmp1.next(__tmp2, __tmp4)

    @classmethod
    def steps(__tmp3, __tmp2) -> typing.List["Step"]:
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
