from typing import TypeAlias
__typ1 : TypeAlias = "HttpResponseNotAllowed"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "JsonableError"

from django.http import HttpResponse, HttpResponseNotAllowed
import ujson

from typing import Optional, Any, Dict, List
from zerver.lib.exceptions import JsonableError

class HttpResponseUnauthorized(__typ2):
    status_code = 401

    def __init__(__tmp2, __tmp6, www_authenticate: Optional[str]=None) :
        __typ2.__init__(__tmp2)
        if www_authenticate is None:
            __tmp2["WWW-Authenticate"] = 'Basic realm="%s"' % (__tmp6,)
        elif www_authenticate == "session":
            __tmp2["WWW-Authenticate"] = 'Session realm="%s"' % (__tmp6,)
        else:
            raise AssertionError("Invalid www_authenticate value!")

def json_unauthorized(__tmp0: <FILL>, www_authenticate: Optional[str]=None) :
    resp = HttpResponseUnauthorized("zulip", www_authenticate=www_authenticate)
    resp.content = (ujson.dumps({"result": "error",
                                 "msg": __tmp0}) + "\n").encode()
    return resp

def json_method_not_allowed(__tmp1) :
    resp = __typ1(__tmp1)
    resp.content = ujson.dumps({"result": "error",
                                "msg": "Method Not Allowed",
                                "allowed_methods": __tmp1}).encode()
    return resp

def __tmp3(res_type: str="success",
                  msg: str="",
                  data: Optional[Dict[str, Any]]=None,
                  status: int=200) :
    content = {"result": res_type, "msg": msg}
    if data is not None:
        content.update(data)
    return __typ2(content=ujson.dumps(content) + "\n",
                        content_type='application/json', status=status)

def json_success(data: Optional[Dict[str, Any]]=None) :
    return __tmp3(data=data)

def __tmp5(exception) -> __typ2:
    '''
    This should only be needed in middleware; in app code, just raise.

    When app code raises a JsonableError, the JsonErrorHandler
    middleware takes care of transforming it into a response by
    calling this function.
    '''
    return __tmp3('error',
                         msg=exception.msg,
                         data=exception.data,
                         status=exception.http_status_code)

def __tmp4(msg, data: Optional[Dict[str, Any]]=None, status: int=400) :
    return __tmp3(res_type="error", msg=msg, data=data, status=status)
