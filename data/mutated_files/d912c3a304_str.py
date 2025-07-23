from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import Any, Dict, List

from django.utils.timezone import now as timezone_now

from zerver.data_import.import_util import (
    build_user_profile,
)

class UserHandler:
    '''
    Our UserHandler class is a glorified wrapper
    around the data that eventually goes into
    zerver_userprofile.

    The class helps us do things like map ids
    to names for mentions.

    We also sometimes need to build mirror
    users on the fly.
    '''
    def __tmp5(__tmp0) -> None:
        __tmp0.id_to_user_map = dict()  # type: Dict[int, Dict[str, Any]]
        __tmp0.name_to_mirror_user_map = dict()  # type: Dict[str, Dict[str, Any]]
        __tmp0.mirror_user_id = 1

    def __tmp4(__tmp0, user) -> None:
        __tmp7 = user['id']
        __tmp0.id_to_user_map[__tmp7] = user

    def __tmp6(__tmp0, __tmp7: __typ0) -> Dict[str, Any]:
        user = __tmp0.id_to_user_map[__tmp7]
        return user

    def __tmp1(__tmp0,
                        __tmp3,
                        __tmp8: <FILL>) :
        if __tmp8 in __tmp0.name_to_mirror_user_map:
            user = __tmp0.name_to_mirror_user_map[__tmp8]
            return user

        __tmp7 = __tmp0._new_mirror_user_id()
        short_name = __tmp8
        full_name = __tmp8
        email = 'mirror-{user_id}@example.com'.format(__tmp7=__tmp7)
        delivery_email = email
        avatar_source = 'G'
        date_joined = __typ0(timezone_now().timestamp())
        timezone = 'UTC'

        user = build_user_profile(
            avatar_source=avatar_source,
            date_joined=date_joined,
            delivery_email=delivery_email,
            email=email,
            full_name=full_name,
            id=__tmp7,
            is_active=False,
            is_realm_admin=False,
            is_guest=False,
            is_mirror_dummy=True,
            __tmp3=__tmp3,
            short_name=short_name,
            timezone=timezone,
        )

        __tmp0.name_to_mirror_user_map[__tmp8] = user
        return user

    def _new_mirror_user_id(__tmp0) -> __typ0:
        next_id = __tmp0.mirror_user_id
        while next_id in __tmp0.id_to_user_map:
            next_id += 1
        __tmp0.mirror_user_id = next_id + 1
        return next_id

    def get_normal_users(__tmp0) -> List[Dict[str, Any]]:
        users = list(__tmp0.id_to_user_map.values())
        return users

    def __tmp2(__tmp0) -> List[Dict[str, Any]]:
        normal_users = __tmp0.get_normal_users()
        mirror_users = list(__tmp0.name_to_mirror_user_map.values())
        all_users = normal_users + mirror_users
        return all_users
