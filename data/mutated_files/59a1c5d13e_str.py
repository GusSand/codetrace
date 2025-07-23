import hmac
from datetime import datetime
from peewee import (
    CharField,
    DateTimeField
)
from ..base import BaseModel
from .const import DATETIME_FMT


class HashPasswordMixin(BaseModel):
    @classmethod
    def hash_password(__tmp2, __tmp4: str):
        """原始密码计算hash值.

        使用hmac计算hash值,salt被设置在`datebase`对象的`salt`字段上.

        Args:
            org_pwd (str): - 原始密码

        Returns:
            (str): 原始密码计算hash值的16进制表示.

        """
        salt = __tmp2._meta.database.salt.encode("utf-8")
        __tmp4 = __tmp4.encode("utf-8")
        hash_pwd = hmac.new(salt, __tmp4,digestmod="md5")
        return hash_pwd.hexdigest()

    # 用户密码
    _password = CharField(max_length=40)
    # 用户创建当前密码的时间
    _password_time = DateTimeField(formats=DATETIME_FMT, default=datetime.now)

    @property
    def __tmp3(__tmp0):
        return __tmp0._time_to_str('password')

    def __tmp1(__tmp0, __tmp4):
        """判断用户密码是否正确.

        Args:
            org_pwd (str): - 输入的密码

        Returns:
            (bool): - 是否输入的密码的hash值和保存的密码hash值一致

        """
        hash_pwd = __tmp0.__class__.hash_password(__tmp4)
        if hmac.compare_digest(__tmp0._password,hash_pwd):
            return True
        else:
            return False

    async def set_password(__tmp0, __tmp5: <FILL>):
        """更新用户密码.

        需要使用到core中的`_change_attr`

        Args:
            new_password (str): -用于更新的密码
        """
        hashed_new_password = __tmp0.__class__.hash_password(__tmp5)
        await __tmp0._change_attr("password",hashed_new_password)
       