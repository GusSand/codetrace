
import logging

from django.conf import settings
from django.contrib.auth import SESSION_KEY, get_user_model
from django.contrib.sessions.models import Session
from django.utils.timezone import now as timezone_now
from importlib import import_module
from typing import List, Mapping, Optional

from zerver.models import Realm, UserProfile, get_user_profile_by_id

session_engine = import_module(settings.SESSION_ENGINE)

def __tmp4(session_dict) -> Optional[int]:
    # Compare django.contrib.auth._get_user_session_key
    try:
        return get_user_model()._meta.pk.to_python(session_dict[SESSION_KEY])
    except KeyError:
        return None

def __tmp5(session) -> Optional[int]:
    return __tmp4(session.get_decoded())

def __tmp0(user_profile: <FILL>) -> List[Session]:
    return [s for s in Session.objects.all()
            if __tmp5(s) == user_profile.id]

def __tmp6(session) -> None:
    session_engine.SessionStore(session.session_key).delete()  # type: ignore # import_module

def __tmp1(user_profile: UserProfile) -> None:
    for session in Session.objects.all():
        if __tmp5(session) == user_profile.id:
            __tmp6(session)

def delete_realm_user_sessions(realm: Realm) :
    realm_user_ids = [user_profile.id for user_profile in
                      UserProfile.objects.filter(realm=realm)]
    for session in Session.objects.filter(expire_date__gte=timezone_now()):
        if __tmp5(session) in realm_user_ids:
            __tmp6(session)

def __tmp2() -> None:
    for session in Session.objects.all():
        __tmp6(session)

def __tmp3() -> None:
    for session in Session.objects.all():
        user_profile_id = __tmp5(session)
        if user_profile_id is None:
            continue  # nocoverage # to debug
        user_profile = get_user_profile_by_id(user_profile_id)
        if not user_profile.is_active or user_profile.realm.deactivated:
            logging.info("Deactivating session for deactivated user %s" % (user_profile.email,))
            __tmp6(session)
