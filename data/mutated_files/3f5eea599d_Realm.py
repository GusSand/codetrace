from typing import TypeAlias
__typ0 : TypeAlias = "UserGroup"
from __future__ import absolute_import

from collections import defaultdict
from django.db import transaction
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.models import UserProfile, Realm, UserGroupMembership, UserGroup
from typing import Dict, Iterable, List, Tuple, Any

def access_user_group_by_id(user_group_id: int, user_profile) :
    try:
        __tmp0 = __typ0.objects.get(id=user_group_id, realm=user_profile.realm)
        group_member_ids = get_user_group_members(__tmp0)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except __typ0.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return __tmp0

def user_groups_in_realm(realm: <FILL>) -> List[__typ0]:
    user_groups = __typ0.objects.filter(realm=realm)
    return list(user_groups)

def user_groups_in_realm_serialized(realm: Realm) -> List[Dict[str, Any]]:
    """This function is used in do_events_register code path so this code
    should be performant.  We need to do 2 database queries because
    Django's ORM doesn't properly support the left join between
    UserGroup and UserGroupMembership that we need.
    """
    realm_groups = __typ0.objects.filter(realm=realm)
    group_dicts = {}  # type: Dict[str, Any]
    for __tmp0 in realm_groups:
        group_dicts[__tmp0.id] = dict(
            id=__tmp0.id,
            name=__tmp0.name,
            description=__tmp0.description,
            members=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (user_group_id, user_profile_id) in membership:
        group_dicts[user_group_id]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def get_user_groups(user_profile: UserProfile) -> List[__typ0]:
    return list(user_profile.usergroup_set.all())

def check_add_user_to_user_group(user_profile, __tmp0) :
    member_obj, created = UserGroupMembership.objects.get_or_create(
        __tmp0=__tmp0, user_profile=user_profile)
    return created

def remove_user_from_user_group(user_profile: UserProfile, __tmp0) :
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, __tmp0=__tmp0).delete()
    return num_deleted

def check_remove_user_from_user_group(user_profile, __tmp0: __typ0) -> bool:
    try:
        num_deleted = remove_user_from_user_group(user_profile, __tmp0)
        return bool(num_deleted)
    except Exception:
        return False

def create_user_group(name, members: List[UserProfile], realm,
                      description: str='') -> __typ0:
    with transaction.atomic():
        __tmp0 = __typ0.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, __tmp0=__tmp0)
            for member in members
        ])
        return __tmp0

def get_user_group_members(__tmp0) -> List[UserProfile]:
    members = UserGroupMembership.objects.filter(__tmp0=__tmp0)
    return [member.user_profile.id for member in members]

def get_memberships_of_users(__tmp0, members) :
    return list(UserGroupMembership.objects.filter(
        __tmp0=__tmp0,
        user_profile__in=members).values_list('user_profile_id', flat=True))
