
from django.http import HttpResponse, HttpRequest

from typing import List
from zerver.models import UserProfile

from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success
from zerver.lib.validator import check_list, check_string

from zerver.lib.actions import do_add_alert_words, do_remove_alert_words
from zerver.lib.alert_words import user_alert_words

def __tmp0(request, __tmp1: UserProfile) -> HttpResponse:
    return json_success({'alert_words': user_alert_words(__tmp1)})

def __tmp2(alert_words) -> List[str]:
    alert_words = [w.strip() for w in alert_words]
    return [w for w in alert_words if w != ""]

@has_request_variables
def add_alert_words(request: HttpRequest, __tmp1: UserProfile,
                    alert_words: List[str]=REQ(validator=check_list(check_string))
                    ) -> HttpResponse:
    do_add_alert_words(__tmp1, __tmp2(alert_words))
    return json_success({'alert_words': user_alert_words(__tmp1)})

@has_request_variables
def remove_alert_words(request: <FILL>, __tmp1,
                       alert_words: List[str]=REQ(validator=check_list(check_string))
                       ) -> HttpResponse:
    do_remove_alert_words(__tmp1, alert_words)
    return json_success({'alert_words': user_alert_words(__tmp1)})
