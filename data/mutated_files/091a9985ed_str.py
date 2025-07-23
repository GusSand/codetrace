from datetime import datetime


class __typ0:

    @classmethod
    async def create_user(__tmp2, *,
                          __tmp0: <FILL>,
                          __tmp1: str,
                          email,
                          access_authority: str=None,
                          role: str=None)->None:
        now_str = datetime.now().strftime(__tmp2.DATETIME_FMT)
        data = {
            '_nickname': __tmp0,
            '_password': __tmp2.hash_password(__tmp1),
            '_email': email
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
