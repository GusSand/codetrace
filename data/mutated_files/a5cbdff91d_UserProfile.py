from typing import TypeAlias
__typ2 : TypeAlias = "Realm"
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
def __tmp2(text: __typ1) -> __typ1:
    translated = text

    for emoticon in EMOTICON_CONVERSIONS:
        translated = re.sub(re.escape(emoticon), EMOTICON_CONVERSIONS[emoticon], translated)

    return translated

def __tmp4(realm: __typ2, __tmp1) :
    realm_emojis = realm.get_active_emoji()
    realm_emoji = realm_emojis.get(__tmp1)
    if realm_emoji is not None:
        return __typ1(realm_emojis[__tmp1]['id']), Reaction.REALM_EMOJI
    if __tmp1 == 'zulip':
        return __tmp1, Reaction.ZULIP_EXTRA_EMOJI
    if __tmp1 in name_to_codepoint:
        return name_to_codepoint[__tmp1], Reaction.UNICODE_EMOJI
    raise JsonableError(_("Emoji '%s' does not exist" % (__tmp1,)))

def __tmp0(realm: __typ2, __tmp1) :
    __tmp4(realm, __tmp1)

def check_emoji_request(realm: __typ2, __tmp1, emoji_code: __typ1,
                        emoji_type) -> None:
    # For a given realm and emoji type, checks whether an emoji
    # code is valid for new reactions, or not.
    if emoji_type == "realm_emoji":
        realm_emojis = realm.get_emoji()
        realm_emoji = realm_emojis.get(emoji_code)
        if realm_emoji is None:
            raise JsonableError(_("Invalid custom emoji."))
        if realm_emoji["name"] != __tmp1:
            raise JsonableError(_("Invalid custom emoji name."))
        if realm_emoji["deactivated"]:
            raise JsonableError(_("This custom emoji has been deactivated."))
    elif emoji_type == "zulip_extra_emoji":
        if emoji_code not in ["zulip"]:
            raise JsonableError(_("Invalid emoji code."))
        if __tmp1 != emoji_code:
            raise JsonableError(_("Invalid emoji name."))
    elif emoji_type == "unicode_emoji":
        if emoji_code not in codepoint_to_name:
            raise JsonableError(_("Invalid emoji code."))
        if name_to_codepoint.get(__tmp1) != emoji_code:
            raise JsonableError(_("Invalid emoji name."))
    else:
        # The above are the only valid emoji types
        raise JsonableError(_("Invalid emoji type."))

def check_emoji_admin(user_profile: <FILL>, __tmp1: Optional[__typ1]=None) :
    """Raises an exception if the user cannot administer the target realm
    emoji name in their organization."""

    # Realm administrators can always administer emoji
    if user_profile.is_realm_admin:
        return
    if user_profile.realm.add_emoji_by_admins_only:
        raise JsonableError(_("Must be an organization administrator"))

    # Otherwise, normal users can add emoji
    if __tmp1 is None:
        return

    # Additionally, normal users can remove emoji they themselves added
    emoji = RealmEmoji.objects.filter(realm=user_profile.realm,
                                      name=__tmp1,
                                      deactivated=False).first()
    current_user_is_author = (emoji is not None and
                              emoji.author is not None and
                              emoji.author.id == user_profile.id)
    if not user_profile.is_realm_admin and not current_user_is_author:
        raise JsonableError(_("Must be an organization administrator or emoji author"))

def __tmp6(__tmp1: __typ1) :
    if re.match(r'^[0-9a-z.\-_]+(?<![.\-_])$', __tmp1):
        return
    raise JsonableError(_("Invalid characters in emoji name"))

def get_emoji_url(__tmp3: __typ1, __tmp5: __typ0) -> __typ1:
    return upload_backend.get_emoji_url(__tmp3, __tmp5)


def get_emoji_file_name(__tmp3: __typ1, emoji_id) -> __typ1:
    _, image_ext = os.path.splitext(__tmp3)
    return ''.join((__typ1(emoji_id), image_ext))
