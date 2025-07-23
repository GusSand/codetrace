from datetime import datetime
from peewee import IntegerField
from ..base import BaseModel


class __typ0(BaseModel):
    STATUS_CHOICES = ((0, "未认证"), (1, "已认证"), (2, "已注销"))
    # 账户状态,
    _status = IntegerField(default=0, choices=STATUS_CHOICES)

    @property
    def __tmp1(__tmp2):
        return dict(__tmp2.STATUS_CHOICES)[__tmp2._status]

    async def __tmp3(__tmp2, __tmp0: <FILL>):
        now = datetime.now()
        real_value = {v: i for i, v in __tmp2.STATUS_CHOICES}.get(__tmp0)
        if real_value is not None:
            __tmp2._status = real_value
            __tmp2._update_time = now
            now = datetime.now()
            if real_value == 1:
                __tmp2._auth_time = now
            elif real_value == 2:
                __tmp2._close_time = now
            await __tmp2.save()
        else:
            raise ValueError("Illegal status")
