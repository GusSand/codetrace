from typing import TypeAlias
__typ1 : TypeAlias = "Realm"
__typ0 : TypeAlias = "UserGroup"
from __future__ import absolute_import

from collections import defaultdict
from django.db import transaction
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.models import UserProfile, Realm, UserGroupMembership, UserGroup
from typing import Dict, Iterable, List, Tuple, Any

def __tmp3(__tmp1: int, user_profile) -> __typ0:
    try:
        __tmp2 = __typ0.objects.get(id=__tmp1, realm=user_profile.realm)
        group_member_ids = __tmp4(__tmp2)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except __typ0.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return __tmp2

def __tmp6(realm: __typ1) -> List[__typ0]:
    user_groups = __typ0.objects.filter(realm=realm)
    return list(user_groups)

def user_groups_in_realm_serialized(realm: __typ1) -> List[Dict[str, Any]]:
    """This function is used in do_events_register code path so this code
    should be performant.  We need to do 2 database queries because
    Django's ORM doesn't properly support the left join between
    UserGroup and UserGroupMembership that we need.
    """
    realm_groups = __typ0.objects.filter(realm=realm)
    group_dicts = {}  # type: Dict[str, Any]
    for __tmp2 in realm_groups:
        group_dicts[__tmp2.id] = dict(
            id=__tmp2.id,
            name=__tmp2.name,
            description=__tmp2.description,
            __tmp0=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (__tmp1, user_profile_id) in membership:
        group_dicts[__tmp1]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def __tmp5(user_profile: <FILL>) -> List[__typ0]:
    return list(user_profile.usergroup_set.all())

def check_add_user_to_user_group(user_profile, __tmp2: __typ0) -> bool:
    member_obj, created = UserGroupMembership.objects.get_or_create(
        __tmp2=__tmp2, user_profile=user_profile)
    return created

def remove_user_from_user_group(user_profile: UserProfile, __tmp2: __typ0) -> int:
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, __tmp2=__tmp2).delete()
    return num_deleted

def check_remove_user_from_user_group(user_profile: UserProfile, __tmp2: __typ0) -> bool:
    try:
        num_deleted = remove_user_from_user_group(user_profile, __tmp2)
        return bool(num_deleted)
    except Exception:
        return False

def create_user_group(name, __tmp0: List[UserProfile], realm: __typ1,
                      description: str='') -> __typ0:
    with transaction.atomic():
        __tmp2 = __typ0.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, __tmp2=__tmp2)
            for member in __tmp0
        ])
        return __tmp2

def __tmp4(__tmp2: __typ0) -> List[UserProfile]:
    __tmp0 = UserGroupMembership.objects.filter(__tmp2=__tmp2)
    return [member.user_profile.id for member in __tmp0]

def get_memberships_of_users(__tmp2: __typ0, __tmp0: List[UserProfile]) -> List[int]:
    return list(UserGroupMembership.objects.filter(
        __tmp2=__tmp2,
        user_profile__in=__tmp0).values_list('user_profile_id', flat=True))
