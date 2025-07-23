# pyre-strict

from typing import List

from lowerpines.manager import AbstractManager
from lowerpines.endpoints.group import Group


class __typ0(AbstractManager[Group]):
    def __tmp2(__tmp1) :
        return Group.get_all(__tmp1.gmi)

    def former(__tmp1) :
        return __typ0(__tmp1.gmi, Group.get_former(__tmp1.gmi))

    def join(__tmp1, __tmp0, share_token: <FILL>) :
        return Group.join(__tmp1.gmi, __tmp0, share_token)

    def rejoin(__tmp1, __tmp0) :
        return Group.rejoin(__tmp1.gmi, __tmp0)
