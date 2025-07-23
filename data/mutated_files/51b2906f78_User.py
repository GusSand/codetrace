from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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


def createMessage(__tmp1, status, project: Project):
    groupNames = const.StatusByRole.get(str(status), {}).get("group", [])
    users = list(User.objects.filter(group__name__in=groupNames))
    users += [__tmp1]
    actionStr = const.ProjectStatus[project.status]
    content = messageTpl.format(__tmp1.username, project.name)
    objs = [
        Message(title=f"{project.name} {actionStr}通知", content=content, userId=__tmp1.id)
        for __tmp1 in users
    ]
    Message.objects.bulk_create(objs)


class Audit(object):
    links = __tmp0()

    @classmethod
    def next(__tmp2, __tmp1) :
        try:
            index = __tmp2.links.index(__tmp1)
        except ValueError:
            return
        if len(__tmp2.links) < index + 1:
            return
        return __tmp2.links[index + 1]

    @classmethod
    def prev(__tmp2, __tmp1) :
        try:
            index = __tmp2.links.index(__tmp1)
        except ValueError:
            return None
        if index - 1 < 0:
            return None
        return __tmp2.links[index - 1]


class Step(object):
    def __init__(self, step: int) :
        """
        docstring here
            :param step: Interger
        """
        self.step = step
        self.name = projectStatus[step]

    def ok(self, __tmp1: <FILL>) :
        """
        该用户对此状态的项目是否有权限
        """
        return __tmp1.group.name in const.StatusByRole[str(self.step)]["group"]

    def next(self, __tmp1, project: Project = None) :
        step = self.step
        if self.name == "审核":
            audit = Audit.next(__tmp1)
            if audit:
                return self
        step = self.step + 1
        if project:
            createMessage(__tmp1, step, project)
        return Step(step)

    def prev(self, __tmp1, project: Project = None) -> "Step":
        if self.name == "驳回":
            audit = Audit.prev(__tmp1)
            if audit:
                return self
        step = self.step - 1
        if project:
            createMessage(__tmp1, step, project)
        return Step(step)

    def __call__(self, __tmp1, action, project: Project = None) -> "Step":
        actionName = const.ProjectLogMapReverse[int(action)]
        if actionName not in projectStatus.values():
            return self
        if actionName == "驳回":
            return self.prev(__tmp1, project)
        return self.next(__tmp1, project)

    @classmethod
    def steps(__tmp2, __tmp1) :
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
