from typing import TypeAlias
__typ0 : TypeAlias = "HttpResponse"
"""View definitions of lggr app."""

import logging
import pprint

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.template import loader
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit

logger = logging.getLogger(__name__)


def __tmp2(__tmp0: HttpRequest) -> __typ0:
    """Return page to test some requests.

    :param req: Request object
    :returns: Test page
    """
    tpl = loader.get_template("lggr/index.html.dtl")
    # https://stackoverflow.com/questions/4591525/is-it-possible-to-pass-query-parameters-via-djangos-url-template-tag
    return __typ0(tpl.render({"v1": "value1", "v2": str(timezone.now())}, __tmp0))


def get(__tmp0: <FILL>) -> __typ0:
    """Log get requests.

    :param req: Request object
    :returns: Get log
    """
    request_id = id(__tmp0)
    log = f"""Id: {request_id} get/ Requested >>>>>
req.META:
{pprint.pformat(__tmp0.META)}
req.GET:
{pprint.pformat(__tmp0.GET.dict())}
Id: {request_id} get/ Requested <<<<<
"""
    # logger.warning(f"Id: {request_id} get/ Requested >>>>>")
    # logger.warning(f"Id: {request_id} req.META:")
    # logger.warning(f"Id: {request_id} {pprint.pformat(req.META)}")
    # logger.warning(f"Id: {request_id} req.GET:")
    # logger.warning(f"Id: {request_id} {pprint.pformat(req.GET.dict())}")
    # logger.warning(f"Id: {request_id} get/ Requested <<<<<")
    # TODO: Any other way of logging other than warning?
    logger.warning(log)
    return __typ0(log, content_type="text/plain")


# curl -X POST -d @a.txt localhost:7700/webtools/lggr/post
# TODO: Possible to change key via config?
@ratelimit(  # type: ignore   # disallow_untyped_decorators
    key="header:x-real-ip", rate="1/s", method=ratelimit.UNSAFE, block=True
)
@csrf_exempt  # type: ignore   # disallow_untyped_decorators
def __tmp1(__tmp0: HttpRequest) :
    """Log post requests.

    :param req: Request object
    :returns: Post log
    """
    request_id = id(__tmp0)
    log = f"""Id: {request_id} post/ Requested >>>>>
req.META:
{pprint.pformat(__tmp0.META)}
req.GET:
{pprint.pformat(__tmp0.GET.dict())}
req.body:
{repr(__tmp0.body)}
req.POST:
{pprint.pformat(__tmp0.POST.dict())}
Id: {request_id} post/ Requested <<<<<
"""
    # logger.warning(f"Id: {request_id} post/ Requested >>>>>")
    # logger.warning(f"Id: {request_id} req.META:")
    # logger.warning(f"Id: {request_id} {pprint.pformat(req.META)}")
    # logger.warning(f"Id: {request_id} req.body:")
    # logger.warning(f"Id: {request_id} {repr(req.body)}")
    # logger.warning(f"Id: {request_id} req.POST:")
    # logger.warning(f"Id: {request_id} {pprint.pformat(req.POST.dict())}")
    # logger.warning(f"Id: {request_id} post/ Requested <<<<<")
    logger.warning(log)
    return __typ0(log, content_type="text/plain")
