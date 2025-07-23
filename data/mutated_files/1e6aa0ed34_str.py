from typing import TypeAlias
__typ1 : TypeAlias = "Group"
# pyre-strict

from typing import List

from lowerpines.manager import AbstractManager
from lowerpines.endpoints.group import Group


class __typ0(AbstractManager[__typ1]):
    def _all(__tmp0) -> List[__typ1]:
        return __typ1.get_all(__tmp0.gmi)

    def former(__tmp0) -> "GroupManager":
        return __typ0(__tmp0.gmi, __typ1.get_former(__tmp0.gmi))

    def join(__tmp0, group_id: <FILL>, share_token: str) -> __typ1:
        return __typ1.join(__tmp0.gmi, group_id, share_token)

    def rejoin(__tmp0, group_id: str) :
        return __typ1.rejoin(__tmp0.gmi, group_id)
