"""Views for webtools rootapp."""

from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.template import loader
from django.utils.html import format_html

app_paths = ["export-as-bookmark", "lggr"]


def __tmp1(__tmp0: <FILL>) :
    """Return index page.

    :param req: Request object
    :returns: Root index page
    """
    tpl = loader.get_template("rootapp/index.html.dtl")
    return HttpResponse(
        tpl.render(
            {
                "app_paths": app_paths,
                "repository_url": "https://github.com/10sr/webtools",
                "revision": settings.WEBTOOLS_REVISION or "Unavailable",
            }
        )
    )
    # return HttpResponse(
    #     "\n".join(f"""<p><a href="{path}">{path}</a></p>""" for path in app_paths)
    #     + format_html(
    #         """<p><a href="{url}">Webtools<a/> Revision: {rev}</p>""",
    #         url="https://github.com/10sr/webtools",
    #         rev=settings.WEBTOOLS_REVISION or "Unavailable",
    #     )
    # )
