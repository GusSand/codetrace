from typing import TypeAlias
__typ1 : TypeAlias = "bytes"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "HttpRequest"
__typ3 : TypeAlias = "UserProfile"

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

def __tmp2(__tmp4, __tmp5: <FILL>) :
    if __tmp4 == '' or len(__tmp4) > 4096:
        raise JsonableError(_('Empty or invalid length token'))
    if __tmp5 == PushDeviceToken.APNS:
        # Validate that we can actually decode the token.
        try:
            b64_to_hex(__tmp4)
        except Exception:
            raise JsonableError(_('Invalid APNS token'))

@human_users_only
@has_request_variables
def __tmp3(request, __tmp0,
                          token: __typ1=REQ(),
                          appid: str=REQ(default=settings.ZULIP_IOS_APP_ID)
                          ) :
    __tmp2(token, PushDeviceToken.APNS)
    add_push_device_token(__tmp0, token, PushDeviceToken.APNS, ios_app_id=appid)
    return json_success()

@human_users_only
@has_request_variables
def __tmp1(request: __typ0, __tmp0,
                       token: __typ1=REQ()) :
    __tmp2(token, PushDeviceToken.GCM)
    add_push_device_token(__tmp0, token, PushDeviceToken.GCM)
    return json_success()

@human_users_only
@has_request_variables
def __tmp6(request: __typ0, __tmp0,
                             token: __typ1=REQ()) -> __typ2:
    __tmp2(token, PushDeviceToken.APNS)
    remove_push_device_token(__tmp0, token, PushDeviceToken.APNS)
    return json_success()

@human_users_only
@has_request_variables
def remove_android_reg_id(request: __typ0, __tmp0,
                          token: __typ1=REQ()) :
    __tmp2(token, PushDeviceToken.GCM)
    remove_push_device_token(__tmp0, token, PushDeviceToken.GCM)
    return json_success()
