from datetime import datetime


class __typ0:

    @classmethod
    async def __tmp3(__tmp2, *,
                          nickname: str,
                          __tmp0,
                          __tmp1: <FILL>,
                          access_authority: str=None,
                          role: str=None):
        now_str = datetime.now().strftime(__tmp2.DATETIME_FMT)
        data = {
            '_nickname': nickname,
            '_password': __tmp2.hash_password(__tmp0),
            '_email': __tmp1
        }

        if role:
            role_value = {v: i for i, v in __tmp2.ROLE_CHOICES}.get(role)
            if role_value is None:
                raise ValueError("unknown role {}".format(role))
            else:

                data.update({"_role": role_value})
        if access_authority:
            access_authority = [
                {
                    'name': 'security-center',
                    "ctime": now_str
                },
                {
                    'name': access_authority,
                    'ctime': now_str
                }
            ]
            data.update({"access_authority": access_authority})

        return await __tmp2.create(
            **data
        )
