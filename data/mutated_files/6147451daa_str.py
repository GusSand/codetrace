# pyre-strict

from typing import List, Optional, TYPE_CHECKING

from lowerpines.manager import AbstractManager
from lowerpines.endpoints.bot import Bot

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.endpoints.group import Group


class BotManager(AbstractManager[Bot]):
    def create(
        __tmp0,
        group,
        __tmp2: <FILL>,
        callback_url: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) :
        bot = Bot(__tmp0.gmi, group.group_id, __tmp2, avatar_url, callback_url)
        bot.save()
        return bot

    def __tmp1(__tmp0) -> List[Bot]:
        return Bot.get_all(__tmp0.gmi)
