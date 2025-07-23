from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "HttpRequest"
from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.utils.translation import ugettext as _

from zerver.models import RealmEmoji, UserProfile
from zerver.lib.emoji import check_emoji_admin, check_valid_emoji_name, check_valid_emoji
from zerver.lib.request import JsonableError, REQ, has_request_variables
from zerver.lib.response import json_success, json_error
from zerver.lib.actions import check_add_realm_emoji, do_remove_realm_emoji
from zerver.decorator import require_non_guest_human_user


def list_emoji(request: __typ0, __tmp0: __typ1) -> __typ2:

    # We don't call check_emoji_admin here because the list of realm
    # emoji is public.
    return json_success({'emoji': __tmp0.realm.get_emoji()})


@require_non_guest_human_user
@has_request_variables
def __tmp1(request, __tmp0: __typ1,
                 emoji_name: str=REQ()) -> __typ2:
    emoji_name = emoji_name.strip().replace(' ', '_')
    check_valid_emoji_name(emoji_name)
    check_emoji_admin(__tmp0)
    if RealmEmoji.objects.filter(realm=__tmp0.realm,
                                 name=emoji_name,
                                 deactivated=False).exists():
        return json_error(_("A custom emoji with this name already exists."))
    if len(request.FILES) != 1:
        return json_error(_("You must upload exactly one file."))
    emoji_file = list(request.FILES.values())[0]
    if (settings.MAX_EMOJI_FILE_SIZE * 1024 * 1024) < emoji_file.size:
        return json_error(_("Uploaded file is larger than the allowed limit of %s MB") % (
            settings.MAX_EMOJI_FILE_SIZE))

    realm_emoji = check_add_realm_emoji(__tmp0.realm,
                                        emoji_name,
                                        __tmp0,
                                        emoji_file)
    if realm_emoji is None:
        return json_error(_("Image file upload failed."))
    return json_success()


def delete_emoji(request: __typ0, __tmp0: __typ1,
                 emoji_name: <FILL>) :
    if not RealmEmoji.objects.filter(realm=__tmp0.realm,
                                     name=emoji_name,
                                     deactivated=False).exists():
        raise JsonableError(_("Emoji '%s' does not exist" % (emoji_name,)))
    check_emoji_admin(__tmp0, emoji_name)
    do_remove_realm_emoji(__tmp0.realm, emoji_name)
    return json_success()
