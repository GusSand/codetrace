from typing import TypeAlias
__typ0 : TypeAlias = "str"
from django.conf import settings

from zerver.lib.avatar_hash import gravatar_hash, user_avatar_hash
from zerver.lib.upload import upload_backend
from zerver.models import Realm

def __tmp0(realm: <FILL>) -> __typ0:
    return get_realm_icon_url(realm)

def get_realm_icon_url(realm) -> __typ0:
    if realm.icon_source == 'U':
        return upload_backend.get_realm_icon_url(realm.id, realm.icon_version)
    elif settings.ENABLE_GRAVATAR:
        hash_key = gravatar_hash(realm.string_id)
        return "https://secure.gravatar.com/avatar/%s?d=identicon" % (hash_key,)
    else:
        return settings.DEFAULT_AVATAR_URI+'?version=0'
