from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "Realm"
__typ0 : TypeAlias = "int"

import os
import re
import ujson

from django.conf import settings
from django.utils.translation import ugettext as _
from typing import Optional, Tuple

from zerver.lib.request import JsonableError
from zerver.lib.upload import upload_backend
from zerver.models import Reaction, Realm, RealmEmoji, UserProfile

EMOJI_PATH = os.path.join(settings.STATIC_ROOT, "generated", "emoji")
NAME_TO_CODEPOINT_PATH = os.path.join(EMOJI_PATH, "name_to_codepoint.json")
CODEPOINT_TO_NAME_PATH = os.path.join(EMOJI_PATH, "codepoint_to_name.json")
EMOTICON_CONVERSIONS_PATH = os.path.join(EMOJI_PATH, "emoticon_conversions.json")

with open(NAME_TO_CODEPOINT_PATH) as fp:
    name_to_codepoint = ujson.load(fp)

with open(CODEPOINT_TO_NAME_PATH) as fp:
    codepoint_to_name = ujson.load(fp)

with open(EMOTICON_CONVERSIONS_PATH) as fp:
    EMOTICON_CONVERSIONS = ujson.load(fp)

possible_emoticons = EMOTICON_CONVERSIONS.keys()
possible_emoticon_regexes = map(re.escape, possible_emoticons)  # type: ignore # AnyStr/str issues
terminal_symbols = ',.;?!()\\[\\] "\'\\n\\t'  # type: str # from composebox_typeahead.js
emoticon_regex = ('(?<![^{0}])(?P<emoticon>('.format(terminal_symbols)
                  + ')|('.join(possible_emoticon_regexes)  # type: ignore # AnyStr/str issues
                  + '))(?![^{0}])'.format(terminal_symbols))

# Translates emoticons to their colon syntax, e.g. `:smiley:`.
def __tmp3(text: str) -> str:
    translated = text

    for emoticon in EMOTICON_CONVERSIONS:
        translated = re.sub(re.escape(emoticon), EMOTICON_CONVERSIONS[emoticon], translated)

    return translated

def __tmp5(realm: __typ2, __tmp0: str) -> Tuple[str, str]:
    realm_emojis = realm.get_active_emoji()
    realm_emoji = realm_emojis.get(__tmp0)
    if realm_emoji is not None:
        return str(realm_emojis[__tmp0]['id']), Reaction.REALM_EMOJI
    if __tmp0 == 'zulip':
        return __tmp0, Reaction.ZULIP_EXTRA_EMOJI
    if __tmp0 in name_to_codepoint:
        return name_to_codepoint[__tmp0], Reaction.UNICODE_EMOJI
    raise JsonableError(_("Emoji '%s' does not exist" % (__tmp0,)))

def check_valid_emoji(realm, __tmp0: str) :
    __tmp5(realm, __tmp0)

def __tmp1(realm, __tmp0: str, emoji_code: str,
                        __tmp8: str) -> None:
    # For a given realm and emoji type, checks whether an emoji
    # code is valid for new reactions, or not.
    if __tmp8 == "realm_emoji":
        realm_emojis = realm.get_emoji()
        realm_emoji = realm_emojis.get(emoji_code)
        if realm_emoji is None:
            raise JsonableError(_("Invalid custom emoji."))
        if realm_emoji["name"] != __tmp0:
            raise JsonableError(_("Invalid custom emoji name."))
        if realm_emoji["deactivated"]:
            raise JsonableError(_("This custom emoji has been deactivated."))
    elif __tmp8 == "zulip_extra_emoji":
        if emoji_code not in ["zulip"]:
            raise JsonableError(_("Invalid emoji code."))
        if __tmp0 != emoji_code:
            raise JsonableError(_("Invalid emoji name."))
    elif __tmp8 == "unicode_emoji":
        if emoji_code not in codepoint_to_name:
            raise JsonableError(_("Invalid emoji code."))
        if name_to_codepoint.get(__tmp0) != emoji_code:
            raise JsonableError(_("Invalid emoji name."))
    else:
        # The above are the only valid emoji types
        raise JsonableError(_("Invalid emoji type."))

def check_emoji_admin(__tmp2, __tmp0: Optional[str]=None) -> None:
    """Raises an exception if the user cannot administer the target realm
    emoji name in their organization."""

    # Realm administrators can always administer emoji
    if __tmp2.is_realm_admin:
        return
    if __tmp2.realm.add_emoji_by_admins_only:
        raise JsonableError(_("Must be an organization administrator"))

    # Otherwise, normal users can add emoji
    if __tmp0 is None:
        return

    # Additionally, normal users can remove emoji they themselves added
    emoji = RealmEmoji.objects.filter(realm=__tmp2.realm,
                                      name=__tmp0,
                                      deactivated=False).first()
    current_user_is_author = (emoji is not None and
                              emoji.author is not None and
                              emoji.author.id == __tmp2.id)
    if not __tmp2.is_realm_admin and not current_user_is_author:
        raise JsonableError(_("Must be an organization administrator or emoji author"))

def __tmp6(__tmp0: <FILL>) -> None:
    if re.match(r'^[0-9a-z.\-_]+(?<![.\-_])$', __tmp0):
        return
    raise JsonableError(_("Invalid characters in emoji name"))

def get_emoji_url(__tmp4, realm_id: __typ0) :
    return upload_backend.get_emoji_url(__tmp4, realm_id)


def __tmp7(__tmp4: str, emoji_id) -> str:
    _, image_ext = os.path.splitext(__tmp4)
    return ''.join((str(emoji_id), image_ext))
