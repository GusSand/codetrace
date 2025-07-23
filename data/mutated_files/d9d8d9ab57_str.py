from datetime import datetime


class __typ0:
    @property
    def social_accounts(__tmp2):
        return __tmp2._social_accounts

    async def _set_social_accounts(__tmp2, new_value):
        __tmp2._social_accounts = new_value
        __tmp2._update_time = datetime.now()
        await __tmp2.save()

    async def update_social_accounts(__tmp2, **new_value):
        Limit_value = {
            "google": None,
            "qq": None,
            "weichat": None,
            "weibo": None
        }
        value = __tmp2.social_accounts
        if value:
            Limit_value.update({
                "google": value.get("google"),
                "qq": value.get("qq"),
                "weichat": value.get("weichat"),
                "weibo": value.get("weibo")
            })
        Limit_value.update({
            "google": new_value.get("google"),
            "qq": new_value.get("qq"),
            "weichat": new_value.get("weichat"),
            "weibo": new_value.get("weibo")
        })
        await __tmp2._set_social_accounts(Limit_value)
        return True

    async def __tmp1(__tmp2, __tmp0: <FILL>):
        Limit_value = {
            "google": None,
            "qq": None,
            "weichat": None,
            "weibo": None
        }
        value = __tmp2.social_accounts
        if value:
            Limit_value.update({
                "google": value.get("google"),
                "qq": value.get("qq"),
                "weichat": value.get("weichat"),
                "weibo": value.get("weibo")
            })
        f = Limit_value.get(__tmp0)
        if not f:
            return False
        else:
            Limit_value[__tmp0] = None
            await __tmp2._set_social_accounts(Limit_value)
            return True
