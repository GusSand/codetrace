from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "str"

from django.conf import settings

from zerver.lib.utils import make_safe_digest

from zerver.models import UserProfile

import hashlib

def __tmp1(email: __typ0) :
    """Compute the Gravatar hash for an email address."""
    # Non-ASCII characters aren't permitted by the currently active e-mail
    # RFCs. However, the IETF has published https://tools.ietf.org/html/rfc4952,
    # outlining internationalization of email addresses, and regardless if we
    # typo an address or someone manages to give us a non-ASCII address, let's
    # not error out on it.
    return make_safe_digest(email.lower(), hashlib.md5)

def user_avatar_hash(uid: __typ0) :

    # WARNING: If this method is changed, you may need to do a migration
    # similar to zerver/migrations/0060_move_avatars_to_be_uid_based.py .

    # The salt probably doesn't serve any purpose now.  In the past we
    # used a hash of the email address, not the user ID, and we salted
    # it in order to make the hashing scheme different from Gravatar's.
    user_key = uid + settings.AVATAR_SALT
    return make_safe_digest(user_key, hashlib.sha1)

def user_avatar_path(__tmp0) :

    # WARNING: If this method is changed, you may need to do a migration
    # similar to zerver/migrations/0060_move_avatars_to_be_uid_based.py .
    return user_avatar_path_from_ids(__tmp0.id, __tmp0.realm_id)

def user_avatar_path_from_ids(__tmp2, realm_id: <FILL>) -> __typ0:
    user_id_hash = user_avatar_hash(__typ0(__tmp2))
    return '%s/%s' % (__typ0(realm_id), user_id_hash)
