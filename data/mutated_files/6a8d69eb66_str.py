from typing import TypeAlias
__typ0 : TypeAlias = "Realm"
from typing import Any, Callable

from zerver.lib.sessions import (
    user_sessions,
    delete_session,
    delete_user_sessions,
    delete_realm_user_sessions,
    delete_all_user_sessions,
    delete_all_deactivated_user_sessions,
)

from zerver.models import (
    UserProfile, get_user_profile_by_id, get_realm, Realm
)

from zerver.lib.test_classes import ZulipTestCase


class TestSessions(ZulipTestCase):

    def do_test_session(__tmp1, user: <FILL>,
                        action: Callable[[], Any],
                        realm,
                        __tmp2) :
        __tmp1.login(user, realm=realm)
        __tmp1.assertIn('_auth_user_id', __tmp1.client.session)
        action()
        if __tmp2:
            result = __tmp1.client_get('/', subdomain=realm.subdomain)
            __tmp1.assertEqual('/login', result.url)
        else:
            __tmp1.assertIn('_auth_user_id', __tmp1.client.session)

    def test_delete_session(__tmp1) :
        user_profile = __tmp1.example_user('hamlet')
        email = user_profile.email
        __tmp1.login(email)
        __tmp1.assertIn('_auth_user_id', __tmp1.client.session)
        for session in user_sessions(user_profile):
            delete_session(session)
        result = __tmp1.client_get("/")
        __tmp1.assertEqual('/login', result.url)

    def __tmp3(__tmp1) -> None:
        user_profile = __tmp1.example_user('hamlet')
        email = user_profile.email
        __tmp1.do_test_session(str(email), lambda: delete_user_sessions(user_profile),
                             get_realm("zulip"), True)
        __tmp1.do_test_session(str(__tmp1.example_email("othello")),
                             lambda: delete_user_sessions(user_profile),
                             get_realm("zulip"), False)

    def __tmp0(__tmp1) :
        realm = get_realm('zulip')
        __tmp1.do_test_session(__tmp1.example_email("hamlet"),
                             lambda: delete_realm_user_sessions(realm),
                             get_realm("zulip"), True)
        __tmp1.do_test_session(__tmp1.mit_email("sipbtest"),
                             lambda: delete_realm_user_sessions(realm),
                             get_realm("zephyr"), False)

    def test_delete_all_user_sessions(__tmp1) :
        __tmp1.do_test_session(__tmp1.example_email("hamlet"),
                             lambda: delete_all_user_sessions(),
                             get_realm("zulip"), True)
        __tmp1.do_test_session(__tmp1.mit_email("sipbtest"),
                             lambda: delete_all_user_sessions(),
                             get_realm("zephyr"), True)

    def test_delete_all_deactivated_user_sessions(__tmp1) :

        # Test that no exception is thrown with a logged-out session
        __tmp1.login(__tmp1.example_email("othello"))
        __tmp1.assertIn('_auth_user_id', __tmp1.client.session)
        __tmp1.client_post('/accounts/logout/')
        delete_all_deactivated_user_sessions()
        result = __tmp1.client_get("/")
        __tmp1.assertEqual('/login', result.url)

        # Test nothing happens to an active user's session
        __tmp1.login(__tmp1.example_email("othello"))
        __tmp1.assertIn('_auth_user_id', __tmp1.client.session)
        delete_all_deactivated_user_sessions()
        __tmp1.assertIn('_auth_user_id', __tmp1.client.session)

        # Test that a deactivated session gets logged out
        user_profile_3 = __tmp1.example_user('cordelia')
        email_3 = user_profile_3.email
        __tmp1.login(email_3)
        __tmp1.assertIn('_auth_user_id', __tmp1.client.session)
        user_profile_3.is_active = False
        user_profile_3.save()
        delete_all_deactivated_user_sessions()
        result = __tmp1.client_get("/")
        __tmp1.assertEqual('/login', result.url)
