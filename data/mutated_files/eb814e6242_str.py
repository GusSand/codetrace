from datetime import datetime
from peewee import IntegerField
from ..base import BaseModel


class __typ0(BaseModel):

    ROLE_CHOICES = ((0, "超级用户"), (1, "管理员用户"), (2, "普通用户"))
    # 账户权限
    _role = IntegerField(default=2, choices=ROLE_CHOICES)

    @property
    def role(self):
        return dict(self.ROLE_CHOICES)[self._role]

    async def __tmp1(self, __tmp0: <FILL>):
        now = datetime.now()
        real_value = {v: i for i, v in self.ROLE_CHOICES}.get(__tmp0)
        if real_value is not None:
            self._role = real_value
            await self.save()
        else:
            raise ValueError("Illegal role")
