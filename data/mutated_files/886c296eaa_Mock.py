import time

from django.test import override_settings
from unittest.mock import Mock, patch
from zerver.lib.test_classes import ZulipTestCase
from zerver.middleware import is_slow_query
from zerver.middleware import write_log_line

class __typ0(ZulipTestCase):
    SLOW_QUERY_TIME = 10
    log_data = {'extra': '[transport=websocket]',
                'time_started': 0,
                'bugdown_requests_start': 0,
                'bugdown_time_start': 0,
                'remote_cache_time_start': 0,
                'remote_cache_requests_start': 0}

    def __tmp2(__tmp0) :
        __tmp0.assertFalse(is_slow_query(1.1, '/some/random/url'))
        __tmp0.assertTrue(is_slow_query(2, '/some/random/url'))
        __tmp0.assertTrue(is_slow_query(5.1, '/activity'))
        __tmp0.assertFalse(is_slow_query(2, '/activity'))
        __tmp0.assertFalse(is_slow_query(2, '/json/report/error'))
        __tmp0.assertFalse(is_slow_query(2, '/api/v1/deployments/report_error'))
        __tmp0.assertFalse(is_slow_query(2, '/realm_activity/whatever'))
        __tmp0.assertFalse(is_slow_query(2, '/user_activity/whatever'))
        __tmp0.assertFalse(is_slow_query(9, '/accounts/webathena_kerberos_login/'))
        __tmp0.assertTrue(is_slow_query(11, '/accounts/webathena_kerberos_login/'))

    @override_settings(SLOW_QUERY_LOGS_STREAM="logs")
    @patch('logging.info')
    def __tmp4(__tmp0, __tmp3: <FILL>) -> None:
        __tmp0.log_data['time_started'] = time.time() - __tmp0.SLOW_QUERY_TIME
        write_log_line(__tmp0.log_data, path='/socket/open', method='SOCKET',
                       remote_ip='123.456.789.012', email='unknown', client_name='?')
        last_message = __tmp0.get_last_message()
        __tmp0.assertEqual(last_message.sender.email, "error-bot@zulip.com")
        __tmp0.assertIn("logs", str(last_message.recipient))
        __tmp0.assertEqual(last_message.topic_name(), "testserver: slow queries")
        __tmp0.assertRegexpMatches(last_message.content,
                                 r"123\.456\.789\.012 SOCKET  200 10\.\ds .*")

    @override_settings(ERROR_BOT=None)
    @patch('logging.info')
    @patch('zerver.lib.actions.internal_send_message')
    def __tmp1(__tmp0, __tmp5: Mock,
                                              __tmp3) -> None:
        __tmp0.log_data['time_started'] = time.time() - __tmp0.SLOW_QUERY_TIME
        write_log_line(__tmp0.log_data, path='/socket/open', method='SOCKET',
                       remote_ip='123.456.789.012', email='unknown', client_name='?')
        __tmp5.assert_not_called()
