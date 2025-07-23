from typing import TypeAlias
__typ1 : TypeAlias = "str"
from typing import Any, Dict, List

from django.utils.timezone import now as timezone_now

from zerver.data_import.import_util import (
    build_user_profile,
)

class __typ0:
    '''
    Our UserHandler class is a glorified wrapper
    around the data that eventually goes into
    zerver_userprofile.

    The class helps us do things like map ids
    to names for mentions.

    We also sometimes need to build mirror
    users on the fly.
    '''
    def __tmp3(__tmp0) -> None:
        __tmp0.id_to_user_map = dict()  # type: Dict[int, Dict[str, Any]]
        __tmp0.name_to_mirror_user_map = dict()  # type: Dict[str, Dict[str, Any]]
        __tmp0.mirror_user_id = 1

    def add_user(__tmp0, user) :
        user_id = user['id']
        __tmp0.id_to_user_map[user_id] = user

    def __tmp4(__tmp0, user_id) :
        user = __tmp0.id_to_user_map[user_id]
        return user

    def __tmp1(__tmp0,
                        __tmp2: <FILL>,
                        name) -> Dict[__typ1, Any]:
        if name in __tmp0.name_to_mirror_user_map:
            user = __tmp0.name_to_mirror_user_map[name]
            return user

        user_id = __tmp0._new_mirror_user_id()
        short_name = name
        full_name = name
        email = 'mirror-{user_id}@example.com'.format(user_id=user_id)
        delivery_email = email
        avatar_source = 'G'
        date_joined = int(timezone_now().timestamp())
        timezone = 'UTC'

        user = build_user_profile(
            avatar_source=avatar_source,
            date_joined=date_joined,
            delivery_email=delivery_email,
            email=email,
            full_name=full_name,
            id=user_id,
            is_active=False,
            is_realm_admin=False,
            is_guest=False,
            is_mirror_dummy=True,
            __tmp2=__tmp2,
            short_name=short_name,
            timezone=timezone,
        )

        __tmp0.name_to_mirror_user_map[name] = user
        return user

    def _new_mirror_user_id(__tmp0) :
        next_id = __tmp0.mirror_user_id
        while next_id in __tmp0.id_to_user_map:
            next_id += 1
        __tmp0.mirror_user_id = next_id + 1
        return next_id

    def get_normal_users(__tmp0) :
        users = list(__tmp0.id_to_user_map.values())
        return users

    def get_all_users(__tmp0) :
        normal_users = __tmp0.get_normal_users()
        mirror_users = list(__tmp0.name_to_mirror_user_map.values())
        all_users = normal_users + mirror_users
        return all_users
