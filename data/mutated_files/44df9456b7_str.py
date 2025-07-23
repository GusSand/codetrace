from typing import TypeAlias
__typ2 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "UserGroup"
__typ4 : TypeAlias = "bool"
__typ3 : TypeAlias = "Realm"
from __future__ import absolute_import

from collections import defaultdict
from django.db import transaction
from django.utils.translation import ugettext as _
from zerver.lib.exceptions import JsonableError
from zerver.models import UserProfile, Realm, UserGroupMembership, UserGroup
from typing import Dict, Iterable, List, Tuple, Any

def __tmp4(user_group_id, user_profile) :
    try:
        __tmp2 = __typ1.objects.get(id=user_group_id, realm=user_profile.realm)
        group_member_ids = get_user_group_members(__tmp2)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except __typ1.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return __tmp2

def user_groups_in_realm(realm: __typ3) :
    user_groups = __typ1.objects.filter(realm=realm)
    return list(user_groups)

def __tmp0(realm) -> List[Dict[str, Any]]:
    """This function is used in do_events_register code path so this code
    should be performant.  We need to do 2 database queries because
    Django's ORM doesn't properly support the left join between
    UserGroup and UserGroupMembership that we need.
    """
    realm_groups = __typ1.objects.filter(realm=realm)
    group_dicts = {}  # type: Dict[str, Any]
    for __tmp2 in realm_groups:
        group_dicts[__tmp2.id] = dict(
            id=__tmp2.id,
            name=__tmp2.name,
            description=__tmp2.description,
            __tmp1=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (user_group_id, user_profile_id) in membership:
        group_dicts[user_group_id]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def __tmp7(user_profile: __typ2) :
    return list(user_profile.usergroup_set.all())

def __tmp6(user_profile: __typ2, __tmp2: __typ1) -> __typ4:
    member_obj, created = UserGroupMembership.objects.get_or_create(
        __tmp2=__tmp2, user_profile=user_profile)
    return created

def __tmp5(user_profile: __typ2, __tmp2: __typ1) :
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, __tmp2=__tmp2).delete()
    return num_deleted

def check_remove_user_from_user_group(user_profile: __typ2, __tmp2) :
    try:
        num_deleted = __tmp5(user_profile, __tmp2)
        return __typ4(num_deleted)
    except Exception:
        return False

def create_user_group(name: <FILL>, __tmp1, realm,
                      description: str='') :
    with transaction.atomic():
        __tmp2 = __typ1.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, __tmp2=__tmp2)
            for member in __tmp1
        ])
        return __tmp2

def get_user_group_members(__tmp2) :
    __tmp1 = UserGroupMembership.objects.filter(__tmp2=__tmp2)
    return [member.user_profile.id for member in __tmp1]

def __tmp3(__tmp2: __typ1, __tmp1) :
    return list(UserGroupMembership.objects.filter(
        __tmp2=__tmp2,
        user_profile__in=__tmp1).values_list('user_profile_id', flat=True))
