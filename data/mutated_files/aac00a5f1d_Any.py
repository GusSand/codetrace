
import ujson

from django.http import HttpResponse
from mock import patch
from typing import Any, Dict

from zerver.lib.test_classes import ZulipTestCase
from zerver.lib.users import get_api_key
from zerver.models import get_user, get_realm


class ZephyrTest(ZulipTestCase):
    def __tmp6(__tmp0) :
        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)

        def __tmp2(__tmp4: Any, **kwargs: Any) -> HttpResponse:
            params = {k: ujson.dumps(v) for k, v in kwargs.items()}
            return __tmp0.client_post('/accounts/webathena_kerberos_login/', params,
                                    __tmp4=__tmp4)

        result = __tmp2("zulip")
        __tmp0.assert_json_error(result, 'Could not find Kerberos credential')

        result = __tmp2("zulip", cred='whatever')
        __tmp0.assert_json_error(result, 'Webathena login not enabled')

        email = str(__tmp0.mit_email("starnine"))
        realm = get_realm('zephyr')
        user = get_user(email, realm)
        api_key = get_api_key(user)
        __tmp0.login(email, realm=realm)

        def ccache_mock(**kwargs: Any) :
            return patch('zerver.views.zephyr.make_ccache', **kwargs)

        def __tmp1(**kwargs: <FILL>) -> Any:
            return patch('zerver.views.zephyr.subprocess.check_call', **kwargs)

        def __tmp3() -> Any:
            return __tmp0.settings(PERSONAL_ZMIRROR_SERVER='server')

        def logging_mock() -> Any:
            return patch('logging.exception')

        cred = dict(cname=dict(nameString=['starnine']))

        with ccache_mock(side_effect=KeyError('foo')):
            result = __tmp2("zephyr", cred=cred)
        __tmp0.assert_json_error(result, 'Invalid Kerberos cache')

        with \
                ccache_mock(return_value=b'1234'), \
                __tmp1(side_effect=KeyError('foo')), \
                logging_mock() as log:
            result = __tmp2("zephyr", cred=cred)

        __tmp0.assert_json_error(result, 'We were unable to setup mirroring for you')
        log.assert_called_with("Error updating the user's ccache")

        with ccache_mock(return_value=b'1234'), __tmp3(), __tmp1() as ssh:
            result = __tmp2("zephyr", cred=cred)

        __tmp0.assert_json_success(result)
        ssh.assert_called_with([
            'ssh',
            'server',
            '--',
            '/home/zulip/python-zulip-api/zulip/integrations/zephyr/process_ccache',
            'starnine',
            api_key,
            'MTIzNA=='])

        # Accounts whose Kerberos usernames are known not to match their
        # zephyr accounts are hardcoded, and should be handled properly.

        def __tmp5() -> Any:
            return patch(
                'zerver.views.zephyr.kerberos_alter_egos',
                {'kerberos_alter_ego': 'starnine'})

        cred = dict(cname=dict(nameString=['kerberos_alter_ego']))
        with \
                ccache_mock(return_value=b'1234'), \
                __tmp3(), \
                __tmp1() as ssh, \
                __tmp5():
            result = __tmp2("zephyr", cred=cred)

        __tmp0.assert_json_success(result)
        ssh.assert_called_with([
            'ssh',
            'server',
            '--',
            '/home/zulip/python-zulip-api/zulip/integrations/zephyr/process_ccache',
            'starnine',
            api_key,
            'MTIzNA=='])
