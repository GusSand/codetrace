from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

    def do_test_session(__tmp0, user: __typ0,
                        __tmp3: Callable[[], Any],
                        realm: <FILL>,
                        __tmp1) :
        __tmp0.login(user, realm=realm)
        __tmp0.assertIn('_auth_user_id', __tmp0.client.session)
        __tmp3()
        if __tmp1:
            result = __tmp0.client_get('/', subdomain=realm.subdomain)
            __tmp0.assertEqual('/login', result.url)
        else:
            __tmp0.assertIn('_auth_user_id', __tmp0.client.session)

    def __tmp5(__tmp0) :
        user_profile = __tmp0.example_user('hamlet')
        email = user_profile.email
        __tmp0.login(email)
        __tmp0.assertIn('_auth_user_id', __tmp0.client.session)
        for session in user_sessions(user_profile):
            delete_session(session)
        result = __tmp0.client_get("/")
        __tmp0.assertEqual('/login', result.url)

    def test_delete_user_sessions(__tmp0) :
        user_profile = __tmp0.example_user('hamlet')
        email = user_profile.email
        __tmp0.do_test_session(__typ0(email), lambda: delete_user_sessions(user_profile),
                             get_realm("zulip"), True)
        __tmp0.do_test_session(__typ0(__tmp0.example_email("othello")),
                             lambda: delete_user_sessions(user_profile),
                             get_realm("zulip"), False)

    def test_delete_realm_user_sessions(__tmp0) -> None:
        realm = get_realm('zulip')
        __tmp0.do_test_session(__tmp0.example_email("hamlet"),
                             lambda: delete_realm_user_sessions(realm),
                             get_realm("zulip"), True)
        __tmp0.do_test_session(__tmp0.mit_email("sipbtest"),
                             lambda: delete_realm_user_sessions(realm),
                             get_realm("zephyr"), False)

    def __tmp2(__tmp0) -> None:
        __tmp0.do_test_session(__tmp0.example_email("hamlet"),
                             lambda: delete_all_user_sessions(),
                             get_realm("zulip"), True)
        __tmp0.do_test_session(__tmp0.mit_email("sipbtest"),
                             lambda: delete_all_user_sessions(),
                             get_realm("zephyr"), True)

    def __tmp4(__tmp0) :

        # Test that no exception is thrown with a logged-out session
        __tmp0.login(__tmp0.example_email("othello"))
        __tmp0.assertIn('_auth_user_id', __tmp0.client.session)
        __tmp0.client_post('/accounts/logout/')
        delete_all_deactivated_user_sessions()
        result = __tmp0.client_get("/")
        __tmp0.assertEqual('/login', result.url)

        # Test nothing happens to an active user's session
        __tmp0.login(__tmp0.example_email("othello"))
        __tmp0.assertIn('_auth_user_id', __tmp0.client.session)
        delete_all_deactivated_user_sessions()
        __tmp0.assertIn('_auth_user_id', __tmp0.client.session)

        # Test that a deactivated session gets logged out
        user_profile_3 = __tmp0.example_user('cordelia')
        email_3 = user_profile_3.email
        __tmp0.login(email_3)
        __tmp0.assertIn('_auth_user_id', __tmp0.client.session)
        user_profile_3.is_active = False
        user_profile_3.save()
        delete_all_deactivated_user_sessions()
        result = __tmp0.client_get("/")
        __tmp0.assertEqual('/login', result.url)
