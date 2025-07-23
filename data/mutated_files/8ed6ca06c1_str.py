from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "int"

from django.conf import settings

from zerver.lib.utils import make_safe_digest

from zerver.models import UserProfile

import hashlib

def __tmp1(__tmp0) :
    """Compute the Gravatar hash for an email address."""
    # Non-ASCII characters aren't permitted by the currently active e-mail
    # RFCs. However, the IETF has published https://tools.ietf.org/html/rfc4952,
    # outlining internationalization of email addresses, and regardless if we
    # typo an address or someone manages to give us a non-ASCII address, let's
    # not error out on it.
    return make_safe_digest(__tmp0.lower(), hashlib.md5)

def __tmp2(__tmp5: <FILL>) :

    # WARNING: If this method is changed, you may need to do a migration
    # similar to zerver/migrations/0060_move_avatars_to_be_uid_based.py .

    # The salt probably doesn't serve any purpose now.  In the past we
    # used a hash of the email address, not the user ID, and we salted
    # it in order to make the hashing scheme different from Gravatar's.
    user_key = __tmp5 + settings.AVATAR_SALT
    return make_safe_digest(user_key, hashlib.sha1)

def __tmp6(user_profile) :

    # WARNING: If this method is changed, you may need to do a migration
    # similar to zerver/migrations/0060_move_avatars_to_be_uid_based.py .
    return __tmp4(user_profile.id, user_profile.realm_id)

def __tmp4(__tmp3, realm_id: __typ0) :
    user_id_hash = __tmp2(str(__tmp3))
    return '%s/%s' % (str(realm_id), user_id_hash)
