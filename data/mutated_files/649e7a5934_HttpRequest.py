from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "HttpResponse"
from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpRequest

from zerver.decorator import require_realm_admin
from zerver.lib.actions import do_change_icon_source
from zerver.lib.realm_icon import realm_icon_url
from zerver.lib.response import json_error, json_success
from zerver.lib.upload import upload_icon_image
from zerver.models import UserProfile


@require_realm_admin
def upload_icon(request, __tmp0) :

    if len(request.FILES) != 1:
        return json_error(_("You must upload exactly one icon."))

    icon_file = list(request.FILES.values())[0]
    if ((settings.MAX_ICON_FILE_SIZE * 1024 * 1024) < icon_file.size):
        return json_error(_("Uploaded file is larger than the allowed limit of %s MB") % (
            settings.MAX_ICON_FILE_SIZE))
    upload_icon_image(icon_file, __tmp0)
    do_change_icon_source(__tmp0.realm, __tmp0.realm.ICON_UPLOADED)
    icon_url = realm_icon_url(__tmp0.realm)

    json_result = dict(
        icon_url=icon_url
    )
    return json_success(json_result)


@require_realm_admin
def delete_icon_backend(request: HttpRequest, __tmp0: __typ0) :
    # We don't actually delete the icon because it might still
    # be needed if the URL was cached and it is rewrited
    # in any case after next update.
    do_change_icon_source(__tmp0.realm, __tmp0.realm.ICON_FROM_GRAVATAR)
    gravatar_url = realm_icon_url(__tmp0.realm)
    json_result = dict(
        icon_url=gravatar_url
    )
    return json_success(json_result)


def __tmp1(request: <FILL>, __tmp0) -> __typ1:
    url = realm_icon_url(__tmp0.realm)

    # We can rely on the url already having query parameters. Because
    # our templates depend on being able to use the ampersand to
    # add query parameters to our url, get_icon_url does '?version=version_number'
    # hacks to prevent us from having to jump through decode/encode hoops.
    assert '?' in url
    url += '&' + request.META['QUERY_STRING']
    return redirect(url)
