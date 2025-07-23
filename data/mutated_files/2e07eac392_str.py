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
def translate_emoticons(text: <FILL>) -> str:
    translated = text

    for emoticon in EMOTICON_CONVERSIONS:
        translated = re.sub(re.escape(emoticon), EMOTICON_CONVERSIONS[emoticon], translated)

    return translated

def emoji_name_to_emoji_code(realm, emoji_name) :
    realm_emojis = realm.get_active_emoji()
    realm_emoji = realm_emojis.get(emoji_name)
    if realm_emoji is not None:
        return str(realm_emojis[emoji_name]['id']), Reaction.REALM_EMOJI
    if emoji_name == 'zulip':
        return emoji_name, Reaction.ZULIP_EXTRA_EMOJI
    if emoji_name in name_to_codepoint:
        return name_to_codepoint[emoji_name], Reaction.UNICODE_EMOJI
    raise JsonableError(_("Emoji '%s' does not exist" % (emoji_name,)))

def __tmp0(realm, emoji_name) :
    emoji_name_to_emoji_code(realm, emoji_name)

def check_emoji_request(realm, emoji_name: str, emoji_code,
                        emoji_type) :
    # For a given realm and emoji type, checks whether an emoji
    # code is valid for new reactions, or not.
    if emoji_type == "realm_emoji":
        realm_emojis = realm.get_emoji()
        realm_emoji = realm_emojis.get(emoji_code)
        if realm_emoji is None:
            raise JsonableError(_("Invalid custom emoji."))
        if realm_emoji["name"] != emoji_name:
            raise JsonableError(_("Invalid custom emoji name."))
        if realm_emoji["deactivated"]:
            raise JsonableError(_("This custom emoji has been deactivated."))
    elif emoji_type == "zulip_extra_emoji":
        if emoji_code not in ["zulip"]:
            raise JsonableError(_("Invalid emoji code."))
        if emoji_name != emoji_code:
            raise JsonableError(_("Invalid emoji name."))
    elif emoji_type == "unicode_emoji":
        if emoji_code not in codepoint_to_name:
            raise JsonableError(_("Invalid emoji code."))
        if name_to_codepoint.get(emoji_name) != emoji_code:
            raise JsonableError(_("Invalid emoji name."))
    else:
        # The above are the only valid emoji types
        raise JsonableError(_("Invalid emoji type."))

def check_emoji_admin(__tmp1, emoji_name: Optional[str]=None) :
    """Raises an exception if the user cannot administer the target realm
    emoji name in their organization."""

    # Realm administrators can always administer emoji
    if __tmp1.is_realm_admin:
        return
    if __tmp1.realm.add_emoji_by_admins_only:
        raise JsonableError(_("Must be an organization administrator"))

    # Otherwise, normal users can add emoji
    if emoji_name is None:
        return

    # Additionally, normal users can remove emoji they themselves added
    emoji = RealmEmoji.objects.filter(realm=__tmp1.realm,
                                      name=emoji_name,
                                      deactivated=False).first()
    current_user_is_author = (emoji is not None and
                              emoji.author is not None and
                              emoji.author.id == __tmp1.id)
    if not __tmp1.is_realm_admin and not current_user_is_author:
        raise JsonableError(_("Must be an organization administrator or emoji author"))

def check_valid_emoji_name(emoji_name: str) :
    if re.match(r'^[0-9a-z.\-_]+(?<![.\-_])$', emoji_name):
        return
    raise JsonableError(_("Invalid characters in emoji name"))

def get_emoji_url(emoji_file_name, realm_id) :
    return upload_backend.get_emoji_url(emoji_file_name, realm_id)


def get_emoji_file_name(emoji_file_name, emoji_id) :
    _, image_ext = os.path.splitext(emoji_file_name)
    return ''.join((str(emoji_id), image_ext))
