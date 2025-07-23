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

def __tmp7(__tmp3, user_profile) :
    try:
        __tmp2 = __typ0.objects.get(id=__tmp3, realm=user_profile.realm)
        group_member_ids = get_user_group_members(__tmp2)
        msg = _("Only group members and organization administrators can administer this group.")
        if (not user_profile.is_realm_admin and user_profile.id not in group_member_ids):
            raise JsonableError(msg)
    except __typ0.DoesNotExist:
        raise JsonableError(_("Invalid user group"))
    return __tmp2

def __tmp11(realm) :
    user_groups = __typ0.objects.filter(realm=realm)
    return list(user_groups)

def __tmp0(realm) :
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
            __tmp1=[],
        )

    membership = UserGroupMembership.objects.filter(user_group__realm=realm).values_list(
        'user_group_id', 'user_profile_id')
    for (__tmp3, user_profile_id) in membership:
        group_dicts[__tmp3]['members'].append(user_profile_id)
    for group_dict in group_dicts.values():
        group_dict['members'] = sorted(group_dict['members'])

    return sorted(group_dicts.values(), key=lambda group_dict: group_dict['id'])

def __tmp10(user_profile) :
    return list(user_profile.usergroup_set.all())

def __tmp9(user_profile: <FILL>, __tmp2) :
    member_obj, created = UserGroupMembership.objects.get_or_create(
        __tmp2=__tmp2, user_profile=user_profile)
    return created

def __tmp8(user_profile, __tmp2) -> int:
    num_deleted, _ = UserGroupMembership.objects.filter(
        user_profile=user_profile, __tmp2=__tmp2).delete()
    return num_deleted

def __tmp5(user_profile, __tmp2) :
    try:
        num_deleted = __tmp8(user_profile, __tmp2)
        return bool(num_deleted)
    except Exception:
        return False

def __tmp6(name, __tmp1, realm,
                      description: str='') :
    with transaction.atomic():
        __tmp2 = __typ0.objects.create(name=name, realm=realm,
                                              description=description)
        UserGroupMembership.objects.bulk_create([
            UserGroupMembership(user_profile=member, __tmp2=__tmp2)
            for member in __tmp1
        ])
        return __tmp2

def get_user_group_members(__tmp2) :
    __tmp1 = UserGroupMembership.objects.filter(__tmp2=__tmp2)
    return [member.user_profile.id for member in __tmp1]

def __tmp4(__tmp2, __tmp1) :
    return list(UserGroupMembership.objects.filter(
        __tmp2=__tmp2,
        user_profile__in=__tmp1).values_list('user_profile_id', flat=True))
