from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "int"
from django.conf import settings

if False:
    from zerver.models import UserProfile

from typing import Any, Dict, Optional

from zerver.lib.avatar_hash import gravatar_hash, user_avatar_path_from_ids
from zerver.lib.upload import upload_backend, MEDIUM_AVATAR_SIZE
from zerver.models import UserProfile
import urllib

def __tmp6(__tmp1, __tmp7: bool=False, __tmp3: bool=False) :

    return __tmp0(
        __tmp10=__tmp1.id,
        realm_id=__tmp1.realm_id,
        email=__tmp1.email,
        avatar_source=__tmp1.avatar_source,
        avatar_version=__tmp1.avatar_version,
        __tmp7=__tmp7,
        __tmp3=__tmp3,
    )

def avatar_url_from_dict(__tmp8, __tmp7: bool=False) :
    '''
    DEPRECATED: We should start using
                get_avatar_field to populate users,
                particularly for codepaths where the
                client can compute gravatar URLS
                on the client side.
    '''
    url = __tmp5(
        __tmp8['id'],
        __tmp8['avatar_source'],
        __tmp8['realm_id'],
        email=__tmp8['email'],
        __tmp7=__tmp7)
    url += '&version=%d' % (__tmp8['avatar_version'],)
    return url

def __tmp0(__tmp10: __typ0,
                     realm_id,
                     email: str,
                     avatar_source,
                     avatar_version,
                     __tmp7,
                     __tmp3) :
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

    if __tmp3:
        '''
        If our client knows how to calculate gravatar hashes, we
        will return None and let the client compute the gravatar
        url.
        '''
        if settings.ENABLE_GRAVATAR:
            if avatar_source == __typ1.AVATAR_FROM_GRAVATAR:
                return None

    '''
    If we get this far, we'll compute an avatar URL that may be
    either user-uploaded or a gravatar, and then we'll add version
    info to try to avoid stale caches.
    '''
    url = __tmp5(
        __tmp9=__tmp10,
        avatar_source=avatar_source,
        realm_id=realm_id,
        email=email,
        __tmp7=__tmp7,
    )
    url += '&version=%d' % (avatar_version,)
    return url

def __tmp11(email, avatar_version, __tmp7: bool=False) :
    url = __tmp2(email, __tmp7)
    url += '&version=%d' % (avatar_version,)
    return url

def __tmp2(email: <FILL>, __tmp7) :
    if settings.ENABLE_GRAVATAR:
        gravitar_query_suffix = "&s=%s" % (MEDIUM_AVATAR_SIZE,) if __tmp7 else ""
        hash_key = gravatar_hash(email)
        return "https://secure.gravatar.com/avatar/%s?d=identicon%s" % (hash_key, gravitar_query_suffix)
    return settings.DEFAULT_AVATAR_URI+'?x=x'

def __tmp5(__tmp9: __typ0,
                                avatar_source: str,
                                realm_id,
                                email: Optional[str]=None,
                                __tmp7: bool=False) :
    if avatar_source == 'U':
        hash_key = user_avatar_path_from_ids(__tmp9, realm_id)
        return upload_backend.get_avatar_url(hash_key, __tmp7=__tmp7)
    assert email is not None
    return __tmp2(email, __tmp7)

def __tmp4(__tmp1: __typ1) :
    """
    Absolute URLs are used to simplify logic for applications that
    won't be served by browsers, such as rendering GCM notifications.
    """
    avatar = __tmp6(__tmp1)
    # avatar_url can return None if client_gravatar=True, however here we use the default value of False
    assert avatar is not None
    return urllib.parse.urljoin(__tmp1.realm.uri, avatar)
