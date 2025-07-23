from typing import TypeAlias
__typ1 : TypeAlias = "HttpResponseNotAllowed"

from django.http import HttpResponse, HttpResponseNotAllowed
import ujson

from typing import Optional, Any, Dict, List
from zerver.lib.exceptions import JsonableError

class __typ0(HttpResponse):
    status_code = 401

    def __init__(self, realm: str, www_authenticate: Optional[str]=None) :
        HttpResponse.__init__(self)
        if www_authenticate is None:
            self["WWW-Authenticate"] = 'Basic realm="%s"' % (realm,)
        elif www_authenticate == "session":
            self["WWW-Authenticate"] = 'Session realm="%s"' % (realm,)
        else:
            raise AssertionError("Invalid www_authenticate value!")

def json_unauthorized(message: str, www_authenticate: Optional[str]=None) :
    resp = __typ0("zulip", www_authenticate=www_authenticate)
    resp.content = (ujson.dumps({"result": "error",
                                 "msg": message}) + "\n").encode()
    return resp

def json_method_not_allowed(methods: List[str]) :
    resp = __typ1(methods)
    resp.content = ujson.dumps({"result": "error",
                                "msg": "Method Not Allowed",
                                "allowed_methods": methods}).encode()
    return resp

def json_response(res_type: str="success",
                  msg: str="",
                  data: Optional[Dict[str, Any]]=None,
                  status: int=200) -> HttpResponse:
    content = {"result": res_type, "msg": msg}
    if data is not None:
        content.update(data)
    return HttpResponse(content=ujson.dumps(content) + "\n",
                        content_type='application/json', status=status)

def json_success(data: Optional[Dict[str, Any]]=None) -> HttpResponse:
    return json_response(data=data)

def __tmp0(exception) -> HttpResponse:
    '''
    This should only be needed in middleware; in app code, just raise.

    When app code raises a JsonableError, the JsonErrorHandler
    middleware takes care of transforming it into a response by
    calling this function.
    '''
    return json_response('error',
                         msg=exception.msg,
                         data=exception.data,
                         status=exception.http_status_code)

def json_error(msg: <FILL>, data: Optional[Dict[str, Any]]=None, status: int=400) :
    return json_response(res_type="error", msg=msg, data=data, status=status)
