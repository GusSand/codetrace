from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "HttpResponse"
from django.http import HttpResponse, HttpRequest
from django.utils.translation import ugettext as _

from typing import List

from zerver.decorator import require_non_guest_human_user
from zerver.context_processors import get_realm_from_request
from zerver.lib.actions import check_add_user_group, do_update_user_group_name, \
    do_update_user_group_description, bulk_add_members_to_user_group, \
    remove_members_from_user_group, check_delete_user_group
from zerver.lib.exceptions import JsonableError
from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success, json_error
from zerver.lib.users import user_ids_to_users
from zerver.lib.validator import check_list, check_string, check_int, \
    check_short_string
from zerver.lib.user_groups import access_user_group_by_id, get_memberships_of_users, \
    get_user_group_members, user_groups_in_realm_serialized
from zerver.models import UserProfile, UserGroup, UserGroupMembership
from zerver.views.streams import compose_views, FuncKwargPair

@require_non_guest_human_user
@has_request_variables
def add_user_group(request: HttpRequest, __tmp2,
                   name: str=REQ(),
                   members: List[int]=REQ(validator=check_list(check_int), default=[]),
                   description: str=REQ()) :
    user_profiles = user_ids_to_users(members, __tmp2.realm)
    check_add_user_group(__tmp2.realm, name, user_profiles, description)
    return json_success()

@require_non_guest_human_user
@has_request_variables
def get_user_group(request: HttpRequest, __tmp2: __typ0) -> __typ1:
    user_groups = user_groups_in_realm_serialized(__tmp2.realm)
    return json_success({"user_groups": user_groups})

@require_non_guest_human_user
@has_request_variables
def __tmp1(request: HttpRequest, __tmp2,
                    __tmp3: int=REQ(validator=check_int),
                    name: str=REQ(default=""), description: str=REQ(default="")
                    ) -> __typ1:
    if not (name or description):
        return json_error(_("No new data supplied"))

    user_group = access_user_group_by_id(__tmp3, __tmp2)

    result = {}
    if name != user_group.name:
        do_update_user_group_name(user_group, name)
        result['name'] = _("Name successfully updated.")

    if description != user_group.description:
        do_update_user_group_description(user_group, description)
        result['description'] = _("Description successfully updated.")

    return json_success(result)

@require_non_guest_human_user
@has_request_variables
def delete_user_group(request, __tmp2,
                      __tmp3: int=REQ(validator=check_int)) -> __typ1:

    check_delete_user_group(__tmp3, __tmp2)
    return json_success()

@require_non_guest_human_user
@has_request_variables
def __tmp5(request: HttpRequest, __tmp2: __typ0,
                              __tmp3: int=REQ(validator=check_int),
                              delete: List[int]=REQ(validator=check_list(check_int), default=[]),
                              add: List[int]=REQ(validator=check_list(check_int), default=[])
                              ) :
    if not add and not delete:
        return json_error(_('Nothing to do. Specify at least one of "add" or "delete".'))

    method_kwarg_pairs = [
        (__tmp4,
         dict(__tmp3=__tmp3, members=add)),
        (__tmp0,
         dict(__tmp3=__tmp3, members=delete))
    ]  # type: List[FuncKwargPair]
    return compose_views(request, __tmp2, method_kwarg_pairs)

def __tmp4(request: HttpRequest, __tmp2: __typ0,
                                 __tmp3: int, members) :
    if not members:
        return json_success()

    user_group = access_user_group_by_id(__tmp3, __tmp2)
    user_profiles = user_ids_to_users(members, __tmp2.realm)
    existing_member_ids = set(get_memberships_of_users(user_group, user_profiles))

    for __tmp2 in user_profiles:
        if __tmp2.id in existing_member_ids:
            raise JsonableError(_("User %s is already a member of this group" % (__tmp2.id,)))

    bulk_add_members_to_user_group(user_group, user_profiles)
    return json_success()

def __tmp0(request: <FILL>, __tmp2: __typ0,
                                      __tmp3, members) -> __typ1:
    if not members:
        return json_success()

    user_profiles = user_ids_to_users(members, __tmp2.realm)
    user_group = access_user_group_by_id(__tmp3, __tmp2)
    group_member_ids = get_user_group_members(user_group)
    for member in members:
        if (member not in group_member_ids):
            raise JsonableError(_("There is no member '%s' in this user group" % (member,)))

    remove_members_from_user_group(user_group, user_profiles)
    return json_success()
