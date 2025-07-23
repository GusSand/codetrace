from typing import TypeAlias
__typ1 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "int"
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _

from zerver.decorator import require_realm_admin
from zerver.lib.actions import do_add_realm_filter, do_remove_realm_filter
from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success, json_error
from zerver.lib.rest import rest_dispatch as _rest_dispatch
from zerver.lib.validator import check_string
from zerver.models import realm_filters_for_realm, UserProfile, RealmFilter


# Custom realm filters
def list_filters(request, __tmp0) :
    filters = realm_filters_for_realm(__tmp0.realm_id)
    return json_success({'filters': filters})


@require_realm_admin
@has_request_variables
def create_filter(request: HttpRequest, __tmp0: <FILL>, pattern: str=REQ(),
                  url_format_string: str=REQ()) -> __typ1:
    try:
        filter_id = do_add_realm_filter(
            realm=__tmp0.realm,
            pattern=pattern,
            url_format_string=url_format_string
        )
        return json_success({'id': filter_id})
    except ValidationError as e:
        return json_error(e.messages[0], data={"errors": dict(e)})


@require_realm_admin
def delete_filter(request, __tmp0: UserProfile,
                  filter_id: __typ0) -> __typ1:
    try:
        do_remove_realm_filter(realm=__tmp0.realm, id=filter_id)
    except RealmFilter.DoesNotExist:
        return json_error(_('Filter not found'))
    return json_success()
