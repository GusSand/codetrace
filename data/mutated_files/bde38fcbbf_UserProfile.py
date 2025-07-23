from typing import TypeAlias
__typ1 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
from __future__ import absolute_import

from collections import defaultdict
from django.db import transaction
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.models import UserProfile, Realm, UserGroupMembership, UserGroup
from typing import Dict, Iterable, List, Tuple, Any

def __tmp4(__tmp2, user_profile: <FILL>) -> UserGroup:
    try:
        __tmp1 = UserGroup.objects.get(id=__tmp2, realm=user_profile.realm)
        group_member_ids = __tmp5(__tmp1)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except UserGroup.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return __tmp1

def user_groups_in_realm(realm) :
    user_groups = UserGroup.objects.filter(realm=realm)
    return list(user_groups)

def user_groups_in_realm_serialized(realm) :
    """This function is used in do_events_register code path so this code
    should be performant.  We need to do 2 database queries because
    Django's ORM doesn't properly support the left join between
    UserGroup and UserGroupMembership that we need.
    """
    realm_groups = UserGroup.objects.filter(realm=realm)
    group_dicts = {}  # type: Dict[str, Any]
    for __tmp1 in realm_groups:
        group_dicts[__tmp1.id] = dict(
            id=__tmp1.id,
            name=__tmp1.name,
            description=__tmp1.description,
            __tmp0=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (__tmp2, user_profile_id) in membership:
        group_dicts[__tmp2]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def __tmp7(user_profile: UserProfile) :
    return list(user_profile.usergroup_set.all())

def check_add_user_to_user_group(user_profile, __tmp1: UserGroup) :
    member_obj, created = UserGroupMembership.objects.get_or_create(
        __tmp1=__tmp1, user_profile=user_profile)
    return created

def __tmp6(user_profile: UserProfile, __tmp1: UserGroup) -> __typ0:
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, __tmp1=__tmp1).delete()
    return num_deleted

def check_remove_user_from_user_group(user_profile: UserProfile, __tmp1: UserGroup) -> __typ1:
    try:
        num_deleted = __tmp6(user_profile, __tmp1)
        return __typ1(num_deleted)
    except Exception:
        return False

def create_user_group(name, __tmp0: List[UserProfile], realm,
                      description: str='') :
    with transaction.atomic():
        __tmp1 = UserGroup.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, __tmp1=__tmp1)
            for member in __tmp0
        ])
        return __tmp1

def __tmp5(__tmp1: UserGroup) -> List[UserProfile]:
    __tmp0 = UserGroupMembership.objects.filter(__tmp1=__tmp1)
    return [member.user_profile.id for member in __tmp0]

def __tmp3(__tmp1: UserGroup, __tmp0) :
    return list(UserGroupMembership.objects.filter(
        __tmp1=__tmp1,
        user_profile__in=__tmp0).values_list('user_profile_id', flat=True))
