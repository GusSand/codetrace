from typing import TypeAlias
__typ1 : TypeAlias = "HttpRequest"

import re
from typing import Any, Dict

from django.http import HttpRequest
from django.views.debug import SafeExceptionReporterFilter

class __typ0(SafeExceptionReporterFilter):
    def get_post_parameters(__tmp1, request: __typ1) :
        filtered_post = SafeExceptionReporterFilter.get_post_parameters(__tmp1, request).copy()
        filtered_vars = ['content', 'secret', 'password', 'key', 'api-key', 'subject', 'stream',
                         'subscriptions', 'to', 'csrfmiddlewaretoken', 'api_key']

        for var in filtered_vars:
            if var in filtered_post:
                filtered_post[var] = '**********'
        return filtered_post

def __tmp2(__tmp0: <FILL>) -> str:
    return re.sub(r"([a-z_-]+=)([^&]+)([&]|$)", r"\1******\3", __tmp0)
