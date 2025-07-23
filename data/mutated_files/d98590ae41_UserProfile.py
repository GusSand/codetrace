from typing import TypeAlias
__typ1 : TypeAlias = "HttpRequest"
__typ3 : TypeAlias = "HttpResponse"
__typ2 : TypeAlias = "bytes"
__typ0 : TypeAlias = "int"

import requests
import json

from typing import Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.decorator import human_users_only
from zerver.lib.push_notifications import add_push_device_token, \
    b64_to_hex, remove_push_device_token
from zerver.lib.request import has_request_variables, REQ, JsonableError
from zerver.lib.response import json_success, json_error
from zerver.lib.validator import check_string, check_list, check_bool
from zerver.models import PushDeviceToken, UserProfile

def validate_token(__tmp2, __tmp3) -> None:
    if __tmp2 == '' or len(__tmp2) > 4096:
        raise JsonableError(_('Empty or invalid length token'))
    if __tmp3 == PushDeviceToken.APNS:
        # Validate that we can actually decode the token.
        try:
            b64_to_hex(__tmp2)
        except Exception:
            raise JsonableError(_('Invalid APNS token'))

@human_users_only
@has_request_variables
def __tmp1(request: __typ1, __tmp0: UserProfile,
                          token: __typ2=REQ(),
                          appid: str=REQ(default=settings.ZULIP_IOS_APP_ID)
                          ) -> __typ3:
    validate_token(token, PushDeviceToken.APNS)
    add_push_device_token(__tmp0, token, PushDeviceToken.APNS, ios_app_id=appid)
    return json_success()

@human_users_only
@has_request_variables
def add_android_reg_id(request: __typ1, __tmp0: <FILL>,
                       token: __typ2=REQ()) -> __typ3:
    validate_token(token, PushDeviceToken.GCM)
    add_push_device_token(__tmp0, token, PushDeviceToken.GCM)
    return json_success()

@human_users_only
@has_request_variables
def __tmp4(request, __tmp0: UserProfile,
                             token: __typ2=REQ()) -> __typ3:
    validate_token(token, PushDeviceToken.APNS)
    remove_push_device_token(__tmp0, token, PushDeviceToken.APNS)
    return json_success()

@human_users_only
@has_request_variables
def __tmp5(request: __typ1, __tmp0: UserProfile,
                          token: __typ2=REQ()) -> __typ3:
    validate_token(token, PushDeviceToken.GCM)
    remove_push_device_token(__tmp0, token, PushDeviceToken.GCM)
    return json_success()
