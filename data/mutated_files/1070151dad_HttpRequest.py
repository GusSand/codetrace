from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "HttpResponse"

from django.http import HttpResponse, HttpRequest

from typing import List
from zerver.models import UserProfile

from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success
from zerver.lib.validator import check_list, check_string

from zerver.lib.actions import do_add_alert_words, do_remove_alert_words
from zerver.lib.alert_words import user_alert_words

def list_alert_words(request: HttpRequest, __tmp0) :
    return json_success({'alert_words': user_alert_words(__tmp0)})

def __tmp1(alert_words) :
    alert_words = [w.strip() for w in alert_words]
    return [w for w in alert_words if w != ""]

@has_request_variables
def add_alert_words(request: <FILL>, __tmp0,
                    alert_words: List[str]=REQ(validator=check_list(check_string))
                    ) :
    do_add_alert_words(__tmp0, __tmp1(alert_words))
    return json_success({'alert_words': user_alert_words(__tmp0)})

@has_request_variables
def remove_alert_words(request, __tmp0,
                       alert_words: List[str]=REQ(validator=check_list(check_string))
                       ) :
    do_remove_alert_words(__tmp0, alert_words)
    return json_success({'alert_words': user_alert_words(__tmp0)})
