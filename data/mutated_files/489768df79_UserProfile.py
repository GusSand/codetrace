from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "UserGroup"
__typ3 : TypeAlias = "Realm"
__typ1 : TypeAlias = "str"
from __future__ import absolute_import

from collections import defaultdict
from django.db import transaction
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.models import UserProfile, Realm, UserGroupMembership, UserGroup
from typing import Dict, Iterable, List, Tuple, Any

def access_user_group_by_id(user_group_id: int, user_profile: UserProfile) :
    try:
        __tmp1 = __typ0.objects.get(id=user_group_id, realm=user_profile.realm)
        group_member_ids = __tmp0(__tmp1)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except __typ0.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return __tmp1

def user_groups_in_realm(realm: __typ3) -> List[__typ0]:
    user_groups = __typ0.objects.filter(realm=realm)
    return list(user_groups)

def user_groups_in_realm_serialized(realm) :
    """This function is used in do_events_register code path so this code
    should be performant.  We need to do 2 database queries because
    Django's ORM doesn't properly support the left join between
    UserGroup and UserGroupMembership that we need.
    """
    realm_groups = __typ0.objects.filter(realm=realm)
    group_dicts = {}  # type: Dict[str, Any]
    for __tmp1 in realm_groups:
        group_dicts[__tmp1.id] = dict(
            id=__tmp1.id,
            name=__tmp1.name,
            description=__tmp1.description,
            members=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (user_group_id, user_profile_id) in membership:
        group_dicts[user_group_id]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def get_user_groups(user_profile: UserProfile) :
    return list(user_profile.usergroup_set.all())

def check_add_user_to_user_group(user_profile: UserProfile, __tmp1) :
    member_obj, created = UserGroupMembership.objects.get_or_create(
        __tmp1=__tmp1, user_profile=user_profile)
    return created

def remove_user_from_user_group(user_profile: <FILL>, __tmp1) -> int:
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, __tmp1=__tmp1).delete()
    return num_deleted

def __tmp2(user_profile: UserProfile, __tmp1: __typ0) :
    try:
        num_deleted = remove_user_from_user_group(user_profile, __tmp1)
        return __typ2(num_deleted)
    except Exception:
        return False

def create_user_group(name: __typ1, members, realm: __typ3,
                      description: __typ1='') :
    with transaction.atomic():
        __tmp1 = __typ0.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, __tmp1=__tmp1)
            for member in members
        ])
        return __tmp1

def __tmp0(__tmp1: __typ0) -> List[UserProfile]:
    members = UserGroupMembership.objects.filter(__tmp1=__tmp1)
    return [member.user_profile.id for member in members]

def __tmp3(__tmp1: __typ0, members: List[UserProfile]) -> List[int]:
    return list(UserGroupMembership.objects.filter(
        __tmp1=__tmp1,
        user_profile__in=members).values_list('user_profile_id', flat=True))
