from datetime import datetime


class CreateMixin:

    @classmethod
    async def create_user(__tmp0, *,
                          nickname,
                          password: <FILL>,
                          email,
                          access_authority: str=None,
                          role: str=None):
        now_str = datetime.now().strftime(__tmp0.DATETIME_FMT)
        data = {
            '_nickname': nickname,
            '_password': __tmp0.hash_password(password),
            '_email': email
        }

        if role:
            role_value = {v: i for i, v in __tmp0.ROLE_CHOICES}.get(role)
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

        return await __tmp0.create(
            **data
        )
