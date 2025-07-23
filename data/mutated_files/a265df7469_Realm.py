from typing import TypeAlias
__typ2 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"

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
def __tmp2(text: __typ1) :
    translated = text

    for emoticon in EMOTICON_CONVERSIONS:
        translated = re.sub(re.escape(emoticon), EMOTICON_CONVERSIONS[emoticon], translated)

    return translated

def emoji_name_to_emoji_code(realm: Realm, __tmp0) :
    realm_emojis = realm.get_active_emoji()
    realm_emoji = realm_emojis.get(__tmp0)
    if realm_emoji is not None:
        return __typ1(realm_emojis[__tmp0]['id']), Reaction.REALM_EMOJI
    if __tmp0 == 'zulip':
        return __tmp0, Reaction.ZULIP_EXTRA_EMOJI
    if __tmp0 in name_to_codepoint:
        return name_to_codepoint[__tmp0], Reaction.UNICODE_EMOJI
    raise JsonableError(_("Emoji '%s' does not exist" % (__tmp0,)))

def check_valid_emoji(realm: <FILL>, __tmp0) -> None:
    emoji_name_to_emoji_code(realm, __tmp0)

def __tmp1(realm: Realm, __tmp0: __typ1, __tmp7,
                        __tmp8: __typ1) :
    # For a given realm and emoji type, checks whether an emoji
    # code is valid for new reactions, or not.
    if __tmp8 == "realm_emoji":
        realm_emojis = realm.get_emoji()
        realm_emoji = realm_emojis.get(__tmp7)
        if realm_emoji is None:
            raise JsonableError(_("Invalid custom emoji."))
        if realm_emoji["name"] != __tmp0:
            raise JsonableError(_("Invalid custom emoji name."))
        if realm_emoji["deactivated"]:
            raise JsonableError(_("This custom emoji has been deactivated."))
    elif __tmp8 == "zulip_extra_emoji":
        if __tmp7 not in ["zulip"]:
            raise JsonableError(_("Invalid emoji code."))
        if __tmp0 != __tmp7:
            raise JsonableError(_("Invalid emoji name."))
    elif __tmp8 == "unicode_emoji":
        if __tmp7 not in codepoint_to_name:
            raise JsonableError(_("Invalid emoji code."))
        if name_to_codepoint.get(__tmp0) != __tmp7:
            raise JsonableError(_("Invalid emoji name."))
    else:
        # The above are the only valid emoji types
        raise JsonableError(_("Invalid emoji type."))

def __tmp4(user_profile: __typ2, __tmp0: Optional[__typ1]=None) :
    """Raises an exception if the user cannot administer the target realm
    emoji name in their organization."""

    # Realm administrators can always administer emoji
    if user_profile.is_realm_admin:
        return
    if user_profile.realm.add_emoji_by_admins_only:
        raise JsonableError(_("Must be an organization administrator"))

    # Otherwise, normal users can add emoji
    if __tmp0 is None:
        return

    # Additionally, normal users can remove emoji they themselves added
    emoji = RealmEmoji.objects.filter(realm=user_profile.realm,
                                      name=__tmp0,
                                      deactivated=False).first()
    current_user_is_author = (emoji is not None and
                              emoji.author is not None and
                              emoji.author.id == user_profile.id)
    if not user_profile.is_realm_admin and not current_user_is_author:
        raise JsonableError(_("Must be an organization administrator or emoji author"))

def __tmp5(__tmp0: __typ1) :
    if re.match(r'^[0-9a-z.\-_]+(?<![.\-_])$', __tmp0):
        return
    raise JsonableError(_("Invalid characters in emoji name"))

def get_emoji_url(__tmp3: __typ1, realm_id: __typ0) :
    return upload_backend.get_emoji_url(__tmp3, realm_id)


def __tmp6(__tmp3: __typ1, __tmp9: __typ0) -> __typ1:
    _, image_ext = os.path.splitext(__tmp3)
    return ''.join((__typ1(__tmp9), image_ext))
