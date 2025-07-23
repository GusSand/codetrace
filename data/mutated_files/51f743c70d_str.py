from typing import TypeAlias
__typ0 : TypeAlias = "Group"
# pyre-strict

from typing import List

from lowerpines.manager import AbstractManager
from lowerpines.endpoints.group import Group


class GroupManager(AbstractManager[__typ0]):
    def __tmp2(__tmp1) :
        return __typ0.get_all(__tmp1.gmi)

    def former(__tmp1) :
        return GroupManager(__tmp1.gmi, __typ0.get_former(__tmp1.gmi))

    def join(__tmp1, __tmp0: str, share_token) :
        return __typ0.join(__tmp1.gmi, __tmp0, share_token)

    def rejoin(__tmp1, __tmp0: <FILL>) -> __typ0:
        return __typ0.rejoin(__tmp1.gmi, __tmp0)
