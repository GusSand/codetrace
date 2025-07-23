from typing import TypeAlias
__typ1 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "JsonableError"

from django.http import HttpResponse, HttpResponseNotAllowed
import ujson

from typing import Optional, Any, Dict, List
from zerver.lib.exceptions import JsonableError

class HttpResponseUnauthorized(__typ1):
    status_code = 401

    def __init__(__tmp3, __tmp7: <FILL>, www_authenticate: Optional[str]=None) :
        __typ1.__init__(__tmp3)
        if www_authenticate is None:
            __tmp3["WWW-Authenticate"] = 'Basic realm="%s"' % (__tmp7,)
        elif www_authenticate == "session":
            __tmp3["WWW-Authenticate"] = 'Session realm="%s"' % (__tmp7,)
        else:
            raise AssertionError("Invalid www_authenticate value!")

def __tmp8(__tmp0, www_authenticate: Optional[str]=None) :
    resp = HttpResponseUnauthorized("zulip", www_authenticate=www_authenticate)
    resp.content = (ujson.dumps({"result": "error",
                                 "msg": __tmp0}) + "\n").encode()
    return resp

def __tmp2(__tmp1) :
    resp = HttpResponseNotAllowed(__tmp1)
    resp.content = ujson.dumps({"result": "error",
                                "msg": "Method Not Allowed",
                                "allowed_methods": __tmp1}).encode()
    return resp

def __tmp4(res_type: str="success",
                  msg: str="",
                  data: Optional[Dict[str, Any]]=None,
                  status: int=200) :
    content = {"result": res_type, "msg": msg}
    if data is not None:
        content.update(data)
    return __typ1(content=ujson.dumps(content) + "\n",
                        content_type='application/json', status=status)

def __tmp9(data: Optional[Dict[str, Any]]=None) :
    return __tmp4(data=data)

def __tmp6(exception) :
    '''
    This should only be needed in middleware; in app code, just raise.

    When app code raises a JsonableError, the JsonErrorHandler
    middleware takes care of transforming it into a response by
    calling this function.
    '''
    return __tmp4('error',
                         msg=exception.msg,
                         data=exception.data,
                         status=exception.http_status_code)

def __tmp5(msg, data: Optional[Dict[str, Any]]=None, status: int=400) :
    return __tmp4(res_type="error", msg=msg, data=data, status=status)
