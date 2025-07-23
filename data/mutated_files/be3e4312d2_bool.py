from django.conf import settings

if False:
    from zerver.models import UserProfile

from typing import Any, Dict, Optional

from zerver.lib.avatar_hash import gravatar_hash, user_avatar_path_from_ids
from zerver.lib.upload import upload_backend, MEDIUM_AVATAR_SIZE
from zerver.models import UserProfile
import urllib

def __tmp2(__tmp0: UserProfile, __tmp3: bool=False, client_gravatar: bool=False) -> Optional[str]:

    return get_avatar_field(
        user_id=__tmp0.id,
        realm_id=__tmp0.realm_id,
        email=__tmp0.email,
        avatar_source=__tmp0.avatar_source,
        avatar_version=__tmp0.avatar_version,
        __tmp3=__tmp3,
        client_gravatar=client_gravatar,
    )

def avatar_url_from_dict(userdict, __tmp3: bool=False) :
    '''
    DEPRECATED: We should start using
                get_avatar_field to populate users,
                particularly for codepaths where the
                client can compute gravatar URLS
                on the client side.
    '''
    url = __tmp4(
        userdict['id'],
        userdict['avatar_source'],
        userdict['realm_id'],
        email=userdict['email'],
        __tmp3=__tmp3)
    url += '&version=%d' % (userdict['avatar_version'],)
    return url

def get_avatar_field(user_id,
                     realm_id,
                     email,
                     avatar_source: str,
                     avatar_version,
                     __tmp3: <FILL>,
                     client_gravatar) -> Optional[str]:
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
            if avatar_source == UserProfile.AVATAR_FROM_GRAVATAR:
                return None

    '''
    If we get this far, we'll compute an avatar URL that may be
    either user-uploaded or a gravatar, and then we'll add version
    info to try to avoid stale caches.
    '''
    url = __tmp4(
        user_profile_id=user_id,
        avatar_source=avatar_source,
        realm_id=realm_id,
        email=email,
        __tmp3=__tmp3,
    )
    url += '&version=%d' % (avatar_version,)
    return url

def get_gravatar_url(email: str, avatar_version: int, __tmp3: bool=False) :
    url = _get_unversioned_gravatar_url(email, __tmp3)
    url += '&version=%d' % (avatar_version,)
    return url

def _get_unversioned_gravatar_url(email: str, __tmp3: bool) :
    if settings.ENABLE_GRAVATAR:
        gravitar_query_suffix = "&s=%s" % (MEDIUM_AVATAR_SIZE,) if __tmp3 else ""
        hash_key = gravatar_hash(email)
        return "https://secure.gravatar.com/avatar/%s?d=identicon%s" % (hash_key, gravitar_query_suffix)
    return settings.DEFAULT_AVATAR_URI+'?x=x'

def __tmp4(user_profile_id: int,
                                avatar_source: str,
                                realm_id: int,
                                email: Optional[str]=None,
                                __tmp3: bool=False) -> str:
    if avatar_source == 'U':
        hash_key = user_avatar_path_from_ids(user_profile_id, realm_id)
        return upload_backend.get_avatar_url(hash_key, __tmp3=__tmp3)
    assert email is not None
    return _get_unversioned_gravatar_url(email, __tmp3)

def __tmp1(__tmp0) :
    """
    Absolute URLs are used to simplify logic for applications that
    won't be served by browsers, such as rendering GCM notifications.
    """
    avatar = __tmp2(__tmp0)
    # avatar_url can return None if client_gravatar=True, however here we use the default value of False
    assert avatar is not None
    return urllib.parse.urljoin(__tmp0.realm.uri, avatar)
