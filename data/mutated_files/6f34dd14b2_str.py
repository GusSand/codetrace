"""
`minified_js` is taken from `zerver.templatetags.minified_js.py`
"""

from django.conf import settings
from django.template import TemplateSyntaxError

from zerver.templatetags.minified_js import MinifiedJSNode


def minified_js(__tmp0: <FILL>, csp_nonce) :
    if __tmp0 not in settings.JS_SPECS:
        raise TemplateSyntaxError(
            "Invalid argument: no JS file %s".format(__tmp0))

    return MinifiedJSNode(__tmp0, csp_nonce).render({})
