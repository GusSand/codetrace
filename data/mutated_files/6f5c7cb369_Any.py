
import ujson

from django.http import HttpResponse
from mock import patch
from typing import Any, Dict

from zerver.lib.test_classes import ZulipTestCase
from zerver.lib.users import get_api_key
from zerver.models import get_user, get_realm


class __typ0(ZulipTestCase):
    def __tmp8(__tmp1) :
        email = __tmp1.example_email('hamlet')
        __tmp1.login(email)

        def __tmp3(__tmp6: Any, **kwargs) :
            params = {k: ujson.dumps(v) for k, v in kwargs.items()}
            return __tmp1.client_post('/accounts/webathena_kerberos_login/', params,
                                    __tmp6=__tmp6)

        result = __tmp3("zulip")
        __tmp1.assert_json_error(result, 'Could not find Kerberos credential')

        result = __tmp3("zulip", cred='whatever')
        __tmp1.assert_json_error(result, 'Webathena login not enabled')

        email = str(__tmp1.mit_email("starnine"))
        realm = get_realm('zephyr')
        user = get_user(email, realm)
        api_key = get_api_key(user)
        __tmp1.login(email, realm=realm)

        def __tmp0(**kwargs: <FILL>) :
            return patch('zerver.views.zephyr.make_ccache', **kwargs)

        def __tmp2(**kwargs) -> Any:
            return patch('zerver.views.zephyr.subprocess.check_call', **kwargs)

        def __tmp4() -> Any:
            return __tmp1.settings(PERSONAL_ZMIRROR_SERVER='server')

        def __tmp5() :
            return patch('logging.exception')

        cred = dict(cname=dict(nameString=['starnine']))

        with __tmp0(side_effect=KeyError('foo')):
            result = __tmp3("zephyr", cred=cred)
        __tmp1.assert_json_error(result, 'Invalid Kerberos cache')

        with \
                __tmp0(return_value=b'1234'), \
                __tmp2(side_effect=KeyError('foo')), \
                __tmp5() as log:
            result = __tmp3("zephyr", cred=cred)

        __tmp1.assert_json_error(result, 'We were unable to setup mirroring for you')
        log.assert_called_with("Error updating the user's ccache")

        with __tmp0(return_value=b'1234'), __tmp4(), __tmp2() as ssh:
            result = __tmp3("zephyr", cred=cred)

        __tmp1.assert_json_success(result)
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

        def __tmp7() :
            return patch(
                'zerver.views.zephyr.kerberos_alter_egos',
                {'kerberos_alter_ego': 'starnine'})

        cred = dict(cname=dict(nameString=['kerberos_alter_ego']))
        with \
                __tmp0(return_value=b'1234'), \
                __tmp4(), \
                __tmp2() as ssh, \
                __tmp7():
            result = __tmp3("zephyr", cred=cred)

        __tmp1.assert_json_success(result)
        ssh.assert_called_with([
            'ssh',
            'server',
            '--',
            '/home/zulip/python-zulip-api/zulip/integrations/zephyr/process_ccache',
            'starnine',
            api_key,
            'MTIzNA=='])
