from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
from django.conf import settings

if False:
    from zerver.models import UserProfile

from typing import Any, Dict, Optional

from zerver.lib.avatar_hash import gravatar_hash, user_avatar_path_from_ids
from zerver.lib.upload import upload_backend, MEDIUM_AVATAR_SIZE
from zerver.models import UserProfile
import urllib

def avatar_url(__tmp0, __tmp3: __typ2=False, client_gravatar: __typ2=False) -> Optional[str]:

    return get_avatar_field(
        __tmp6=__tmp0.id,
        realm_id=__tmp0.realm_id,
        email=__tmp0.email,
        avatar_source=__tmp0.avatar_source,
        avatar_version=__tmp0.avatar_version,
        __tmp3=__tmp3,
        client_gravatar=client_gravatar,
    )

def __tmp1(__tmp4, __tmp3: __typ2=False) -> str:
    '''
    DEPRECATED: We should start using
                get_avatar_field to populate users,
                particularly for codepaths where the
                client can compute gravatar URLS
                on the client side.
    '''
    url = _get_unversioned_avatar_url(
        __tmp4['id'],
        __tmp4['avatar_source'],
        __tmp4['realm_id'],
        email=__tmp4['email'],
        __tmp3=__tmp3)
    url += '&version=%d' % (__tmp4['avatar_version'],)
    return url

def get_avatar_field(__tmp6: __typ0,
                     realm_id,
                     email: str,
                     avatar_source: <FILL>,
                     avatar_version,
                     __tmp3,
                     client_gravatar) :
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

    if client_gravatar:
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
    url = _get_unversioned_avatar_url(
        __tmp5=__tmp6,
        avatar_source=avatar_source,
        realm_id=realm_id,
        email=email,
        __tmp3=__tmp3,
    )
    url += '&version=%d' % (avatar_version,)
    return url

def __tmp7(email: str, avatar_version, __tmp3: __typ2=False) :
    url = _get_unversioned_gravatar_url(email, __tmp3)
    url += '&version=%d' % (avatar_version,)
    return url

def _get_unversioned_gravatar_url(email, __tmp3: __typ2) -> str:
    if settings.ENABLE_GRAVATAR:
        gravitar_query_suffix = "&s=%s" % (MEDIUM_AVATAR_SIZE,) if __tmp3 else ""
        hash_key = gravatar_hash(email)
        return "https://secure.gravatar.com/avatar/%s?d=identicon%s" % (hash_key, gravitar_query_suffix)
    return settings.DEFAULT_AVATAR_URI+'?x=x'

def _get_unversioned_avatar_url(__tmp5,
                                avatar_source: str,
                                realm_id: __typ0,
                                email: Optional[str]=None,
                                __tmp3: __typ2=False) :
    if avatar_source == 'U':
        hash_key = user_avatar_path_from_ids(__tmp5, realm_id)
        return upload_backend.get_avatar_url(hash_key, __tmp3=__tmp3)
    assert email is not None
    return _get_unversioned_gravatar_url(email, __tmp3)

def __tmp2(__tmp0: __typ1) -> str:
    """
    Absolute URLs are used to simplify logic for applications that
    won't be served by browsers, such as rendering GCM notifications.
    """
    avatar = avatar_url(__tmp0)
    # avatar_url can return None if client_gravatar=True, however here we use the default value of False
    assert avatar is not None
    return urllib.parse.urljoin(__tmp0.realm.uri, avatar)
