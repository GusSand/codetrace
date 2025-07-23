from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "str"
# -*- coding: utf-8 -*-

from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, FileResponse, \
    HttpResponseNotFound
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from zerver.lib.request import has_request_variables, REQ
from zerver.lib.response import json_success, json_error
from zerver.lib.upload import upload_message_image_from_request, get_local_file_path, \
    get_signed_upload_url, get_realm_for_filename, check_upload_within_quota
from zerver.lib.validator import check_bool
from zerver.models import UserProfile, validate_attachment_request
from django.conf import settings
from sendfile import sendfile
from mimetypes import guess_type

def __tmp3(request: HttpRequest, __tmp2) -> __typ2:
    uri = get_signed_upload_url(__tmp2)
    return redirect(uri)

def __tmp1(request: HttpRequest, path_id) -> __typ2:
    local_path = get_local_file_path(path_id)
    if local_path is None:
        return HttpResponseNotFound('<p>File not found</p>')

    # Here we determine whether a browser should treat the file like
    # an attachment (and thus clicking a link to it should download)
    # or like a link (and thus clicking a link to it should display it
    # in a browser tab).  This is controlled by the
    # Content-Disposition header; `django-sendfile` sends the
    # attachment-style version of that header if and only if the
    # attachment argument is passed to it.  For attachments,
    # django-sendfile sets the response['Content-disposition'] like
    # this: `attachment; filename="b'zulip.txt'"; filename*=UTF-8''zulip.txt`.
    #
    # The "filename" field (used to name the file when downloaded) is
    # unreliable because it doesn't have a well-defined encoding; the
    # newer filename* field takes precedence, since it uses a
    # consistent format (urlquoted).  For more details on filename*
    # and filename, see the below docs:
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
    attachment = True
    file_type = guess_type(local_path)[0]
    if file_type is not None and (file_type.startswith("image/") or
                                  file_type == "application/pdf"):
        attachment = False

    return sendfile(request, local_path, attachment=attachment)

def __tmp4(request: HttpRequest, __tmp0,
                       realm_id_str: __typ0, filename: __typ0) -> __typ2:
    path_id = "%s/%s" % (realm_id_str, filename)
    is_authorized = validate_attachment_request(__tmp0, path_id)

    if is_authorized is None:
        return HttpResponseNotFound(_("<p>File not found.</p>"))
    if not is_authorized:
        return HttpResponseForbidden(_("<p>You are not authorized to view this file.</p>"))
    if settings.LOCAL_UPLOADS_DIR is not None:
        return __tmp1(request, path_id)

    return __tmp3(request, path_id)

def upload_file_backend(request: <FILL>, __tmp0: __typ1) -> __typ2:
    if len(request.FILES) == 0:
        return json_error(_("You must specify a file to upload"))
    if len(request.FILES) != 1:
        return json_error(_("You may only upload one file at a time"))

    user_file = list(request.FILES.values())[0]
    file_size = user_file._get_size()
    if settings.MAX_FILE_UPLOAD_SIZE * 1024 * 1024 < file_size:
        return json_error(_("Uploaded file is larger than the allowed limit of %s MB") % (
            settings.MAX_FILE_UPLOAD_SIZE))
    check_upload_within_quota(__tmp0.realm, file_size)

    if not isinstance(user_file.name, __typ0):
        # It seems that in Python 2 unicode strings containing bytes are
        # rendered differently than ascii strings containing same bytes.
        #
        # Example:
        # >>> print('\xd3\x92')
        # Ӓ
        # >>> print(u'\xd3\x92')
        # Ó
        #
        # This is the cause of the problem as user_file.name variable
        # is received as a unicode which is converted into unicode
        # strings containing bytes and is rendered incorrectly.
        #
        # Example:
        # >>> import urllib.parse
        # >>> name = u'%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D0%B5%D0%B8%CC%86%D1%82%D0%B5.txt'
        # >>> print(urllib.parse.unquote(name))
        # ÐÐ´ÑÐ°Ð²ÐµÐ¸ÌÑÐµ  # This is wrong
        #
        # >>> name = '%D0%97%D0%B4%D1%80%D0%B0%D0%B2%D0%B5%D0%B8%CC%86%D1%82%D0%B5.txt'
        # >>> print(urllib.parse.unquote(name))
        # Здравейте.txt  # This is correct
        user_file.name = user_file.name.encode('ascii')

    uri = upload_message_image_from_request(request, user_file, __tmp0)
    return json_success({'uri': uri})
