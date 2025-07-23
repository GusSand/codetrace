from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "UserGroup"
__typ1 : TypeAlias = "str"
from __future__ import absolute_import

from collections import defaultdict
from django.db import transaction
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.models import UserProfile, Realm, UserGroupMembership, UserGroup
from typing import Dict, Iterable, List, Tuple, Any

def __tmp3(__tmp1: <FILL>, user_profile) :
    try:
        user_group = __typ0.objects.get(id=__tmp1, realm=user_profile.realm)
        group_member_ids = get_user_group_members(user_group)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except __typ0.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return user_group

def __tmp4(realm) :
    user_groups = __typ0.objects.filter(realm=realm)
    return list(user_groups)

def user_groups_in_realm_serialized(realm: Realm) :
    """This function is used in do_events_register code path so this code
    should be performant.  We need to do 2 database queries because
    Django's ORM doesn't properly support the left join between
    UserGroup and UserGroupMembership that we need.
    """
    realm_groups = __typ0.objects.filter(realm=realm)
    group_dicts = {}  # type: Dict[str, Any]
    for user_group in realm_groups:
        group_dicts[user_group.id] = dict(
            id=user_group.id,
            name=user_group.name,
            description=user_group.description,
            __tmp0=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (__tmp1, user_profile_id) in membership:
        group_dicts[__tmp1]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def get_user_groups(user_profile: UserProfile) :
    return list(user_profile.usergroup_set.all())

def check_add_user_to_user_group(user_profile, user_group) :
    member_obj, created = UserGroupMembership.objects.get_or_create(
        user_group=user_group, user_profile=user_profile)
    return created

def remove_user_from_user_group(user_profile, user_group) :
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, user_group=user_group).delete()
    return num_deleted

def check_remove_user_from_user_group(user_profile: UserProfile, user_group) :
    try:
        num_deleted = remove_user_from_user_group(user_profile, user_group)
        return __typ2(num_deleted)
    except Exception:
        return False

def create_user_group(name, __tmp0, realm,
                      description: __typ1='') :
    with transaction.atomic():
        user_group = __typ0.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, user_group=user_group)
            for member in __tmp0
        ])
        return user_group

def get_user_group_members(user_group) -> List[UserProfile]:
    __tmp0 = UserGroupMembership.objects.filter(user_group=user_group)
    return [member.user_profile.id for member in __tmp0]

def __tmp2(user_group: __typ0, __tmp0) :
    return list(UserGroupMembership.objects.filter(
        user_group=user_group,
        user_profile__in=__tmp0).values_list('user_profile_id', flat=True))
