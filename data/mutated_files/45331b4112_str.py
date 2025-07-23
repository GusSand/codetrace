from typing import TypeAlias
__typ2 : TypeAlias = "Any"
# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Iterable, List, Tuple

from django.test import override_settings
from zerver.lib.test_classes import (
    ZulipTestCase,
)
from zerver.lib.utils import statsd

import mock
import ujson
import os

def __tmp4(raw_params: Dict[str, __typ2]) -> Dict[str, str]:
    # A few of our few legacy endpoints need their
    # individual parameters serialized as JSON.
    return {k: ujson.dumps(v) for k, v in raw_params.items()}

class __typ1:
    def __tmp3(__tmp0, settings) :
        __tmp0.settings = settings
        __tmp0.real_impl = statsd
        __tmp0.func_calls = []  # type: List[Tuple[str, Iterable[Any]]]

    def __tmp1(__tmp0, __tmp5: <FILL>) -> Callable[..., __typ2]:
        def f(*args) -> None:
            with __tmp0.settings(STATSD_HOST=''):
                getattr(__tmp0.real_impl, __tmp5)(*args)
            __tmp0.func_calls.append((__tmp5, args))

        return f

class __typ0(ZulipTestCase):
    def test_send_time(__tmp0) -> None:
        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)

        params = dict(
            time=5,
            received=6,
            displayed=7,
            locally_echoed='true',
            rendered_content_disparity='true',
        )

        stats_mock = __typ1(__tmp0.settings)
        with mock.patch('zerver.views.report.statsd', wraps=stats_mock):
            result = __tmp0.client_post("/json/report/send_times", params)
        __tmp0.assert_json_success(result)

        expected_calls = [
            ('timing', ('endtoend.send_time.zulip', 5)),
            ('timing', ('endtoend.receive_time.zulip', 6)),
            ('timing', ('endtoend.displayed_time.zulip', 7)),
            ('incr', ('locally_echoed',)),
            ('incr', ('render_disparity',)),
        ]
        __tmp0.assertEqual(stats_mock.func_calls, expected_calls)

    def test_narrow_time(__tmp0) :
        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)

        params = dict(
            initial_core=5,
            initial_free=6,
            network=7,
        )

        stats_mock = __typ1(__tmp0.settings)
        with mock.patch('zerver.views.report.statsd', wraps=stats_mock):
            result = __tmp0.client_post("/json/report/narrow_times", params)
        __tmp0.assert_json_success(result)

        expected_calls = [
            ('timing', ('narrow.initial_core.zulip', 5)),
            ('timing', ('narrow.initial_free.zulip', 6)),
            ('timing', ('narrow.network.zulip', 7)),
        ]
        __tmp0.assertEqual(stats_mock.func_calls, expected_calls)

    def test_unnarrow_time(__tmp0) :
        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)

        params = dict(
            initial_core=5,
            initial_free=6,
        )

        stats_mock = __typ1(__tmp0.settings)
        with mock.patch('zerver.views.report.statsd', wraps=stats_mock):
            result = __tmp0.client_post("/json/report/unnarrow_times", params)
        __tmp0.assert_json_success(result)

        expected_calls = [
            ('timing', ('unnarrow.initial_core.zulip', 5)),
            ('timing', ('unnarrow.initial_free.zulip', 6)),
        ]
        __tmp0.assertEqual(stats_mock.func_calls, expected_calls)

    @override_settings(BROWSER_ERROR_REPORTING=True)
    def __tmp2(__tmp0) :
        email = __tmp0.example_email('hamlet')
        __tmp0.login(email)

        params = __tmp4(dict(
            message='hello',
            stacktrace='trace',
            ui_message=True,
            user_agent='agent',
            href='href',
            log='log',
            more_info=dict(foo='bar', draft_content="**draft**"),
        ))

        publish_mock = mock.patch('zerver.views.report.queue_json_publish')
        subprocess_mock = mock.patch(
            'zerver.views.report.subprocess.check_output',
            side_effect=KeyError('foo')
        )
        with publish_mock as m, subprocess_mock:
            result = __tmp0.client_post("/json/report/error", params)
        __tmp0.assert_json_success(result)

        report = m.call_args[0][1]['report']
        for k in set(params) - set(['ui_message', 'more_info']):
            __tmp0.assertEqual(report[k], params[k])

        __tmp0.assertEqual(report['more_info'], dict(foo='bar', draft_content="'**xxxxx**'"))
        __tmp0.assertEqual(report['user_email'], email)

        # Teset with no more_info
        del params['more_info']
        with publish_mock as m, subprocess_mock:
            result = __tmp0.client_post("/json/report/error", params)
        __tmp0.assert_json_success(result)

        with __tmp0.settings(BROWSER_ERROR_REPORTING=False):
            result = __tmp0.client_post("/json/report/error", params)
        __tmp0.assert_json_success(result)

        # If js_source_map is present, then the stack trace should be annotated.
        # DEVELOPMENT=False and TEST_SUITE=False are necessary to ensure that
        # js_source_map actually gets instantiated.
        with \
                __tmp0.settings(DEVELOPMENT=False, TEST_SUITE=False), \
                mock.patch('zerver.lib.unminify.SourceMap.annotate_stacktrace') as annotate:
            result = __tmp0.client_post("/json/report/error", params)
        __tmp0.assert_json_success(result)
        # fix_params (see above) adds quotes when JSON encoding.
        annotate.assert_called_once_with('"trace"')

    def test_report_csp_violations(__tmp0) -> None:
        fixture_data = __tmp0.fixture_data('csp_report.json')
        result = __tmp0.client_post("/report/csp_violations", fixture_data, content_type="application/json")
        __tmp0.assert_json_success(result)
