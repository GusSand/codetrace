from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "bool"
from django.conf import settings

if False:
    from zerver.models import UserProfile

from typing import Any, Dict, Optional

from zerver.lib.avatar_hash import gravatar_hash, user_avatar_path_from_ids
from zerver.lib.upload import upload_backend, MEDIUM_AVATAR_SIZE
from zerver.models import UserProfile
import urllib

def __tmp8(__tmp2: UserProfile, __tmp6: __typ1=False, __tmp5: __typ1=False) :

    return __tmp1(
        __tmp0=__tmp2.id,
        realm_id=__tmp2.realm_id,
        email=__tmp2.email,
        avatar_source=__tmp2.avatar_source,
        avatar_version=__tmp2.avatar_version,
        __tmp6=__tmp6,
        __tmp5=__tmp5,
    )

def __tmp3(__tmp7: Dict[str, Any], __tmp6: __typ1=False) :
    '''
    DEPRECATED: We should start using
                get_avatar_field to populate users,
                particularly for codepaths where the
                client can compute gravatar URLS
                on the client side.
    '''
    url = __tmp10(
        __tmp7['id'],
        __tmp7['avatar_source'],
        __tmp7['realm_id'],
        email=__tmp7['email'],
        __tmp6=__tmp6)
    url += '&version=%d' % (__tmp7['avatar_version'],)
    return url

def __tmp1(__tmp0,
                     realm_id,
                     email: <FILL>,
                     avatar_source: str,
                     avatar_version,
                     __tmp6: __typ1,
                     __tmp5: __typ1) :
    '''
    Most of the parameters to this function map to fields
    by the same name in UserProfile (avatar_source, realm_id,
    email, etc.).

    Then there are these:

        medium - This means we want a medium-sized avatar. This can
            affect the "s" parameter for gravatar avatars, or it
            can give us something like foo-medium.png for
            user-uploaded avatars.

        client_gravatar - If the client can compute their own
            gravatars, this will be set to True, and we'll avoid
            computing them on the server (mostly to save bandwidth).
    '''

    if __tmp5:
        '''
        If our client knows how to calculate gravatar hashes, we
        will return None and let the client compute the gravatar
        url.
        '''
        if settings.ENABLE_GRAVATAR:
            if avatar_source == UserProfile.AVATAR_FROM_GRAVATAR:
                return None

    '''
    If we get this far, we'll compute an avatar URL that may be
    either user-uploaded or a gravatar, and then we'll add version
    info to try to avoid stale caches.
    '''
    url = __tmp10(
        __tmp9=__tmp0,
        avatar_source=avatar_source,
        realm_id=realm_id,
        email=email,
        __tmp6=__tmp6,
    )
    url += '&version=%d' % (avatar_version,)
    return url

def __tmp11(email, avatar_version: __typ0, __tmp6: __typ1=False) :
    url = __tmp4(email, __tmp6)
    url += '&version=%d' % (avatar_version,)
    return url

def __tmp4(email: str, __tmp6) :
    if settings.ENABLE_GRAVATAR:
        gravitar_query_suffix = "&s=%s" % (MEDIUM_AVATAR_SIZE,) if __tmp6 else ""
        hash_key = gravatar_hash(email)
        return "https://secure.gravatar.com/avatar/%s?d=identicon%s" % (hash_key, gravitar_query_suffix)
    return settings.DEFAULT_AVATAR_URI+'?x=x'

def __tmp10(__tmp9,
                                avatar_source,
                                realm_id,
                                email: Optional[str]=None,
                                __tmp6: __typ1=False) -> str:
    if avatar_source == 'U':
        hash_key = user_avatar_path_from_ids(__tmp9, realm_id)
        return upload_backend.get_avatar_url(hash_key, __tmp6=__tmp6)
    assert email is not None
    return __tmp4(email, __tmp6)

def absolute_avatar_url(__tmp2) :
    """
    Absolute URLs are used to simplify logic for applications that
    won't be served by browsers, such as rendering GCM notifications.
    """
    avatar = __tmp8(__tmp2)
    # avatar_url can return None if client_gravatar=True, however here we use the default value of False
    assert avatar is not None
    return urllib.parse.urljoin(__tmp2.realm.uri, avatar)
