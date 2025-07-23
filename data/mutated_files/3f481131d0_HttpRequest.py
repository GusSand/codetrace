
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

def __tmp2(__tmp3: bytes, kind: int) :
    if __tmp3 == '' or len(__tmp3) > 4096:
        raise JsonableError(_('Empty or invalid length token'))
    if kind == PushDeviceToken.APNS:
        # Validate that we can actually decode the token.
        try:
            b64_to_hex(__tmp3)
        except Exception:
            raise JsonableError(_('Invalid APNS token'))

@human_users_only
@has_request_variables
def __tmp4(request, __tmp0: UserProfile,
                          token: bytes=REQ(),
                          appid: str=REQ(default=settings.ZULIP_IOS_APP_ID)
                          ) -> HttpResponse:
    __tmp2(token, PushDeviceToken.APNS)
    add_push_device_token(__tmp0, token, PushDeviceToken.APNS, ios_app_id=appid)
    return json_success()

@human_users_only
@has_request_variables
def __tmp1(request: <FILL>, __tmp0: UserProfile,
                       token: bytes=REQ()) :
    __tmp2(token, PushDeviceToken.GCM)
    add_push_device_token(__tmp0, token, PushDeviceToken.GCM)
    return json_success()

@human_users_only
@has_request_variables
def __tmp5(request, __tmp0: UserProfile,
                             token: bytes=REQ()) :
    __tmp2(token, PushDeviceToken.APNS)
    remove_push_device_token(__tmp0, token, PushDeviceToken.APNS)
    return json_success()

@human_users_only
@has_request_variables
def remove_android_reg_id(request: HttpRequest, __tmp0: UserProfile,
                          token: bytes=REQ()) :
    __tmp2(token, PushDeviceToken.GCM)
    remove_push_device_token(__tmp0, token, PushDeviceToken.GCM)
    return json_success()
