# -*- coding: utf-8 -*-
from django.conf import settings

from zerver.data_import.slack_message_conversion import (
    convert_to_zulip_markdown,
    get_user_full_name
)
from zerver.lib.test_classes import (
    ZulipTestCase,
)
from zerver.lib.test_runner import slow
from zerver.lib import mdiff
import ujson

import os
from typing import Any, AnyStr, Dict, List, Optional, Set, Tuple

class SlackMessageConversion(ZulipTestCase):
    def assertEqual(__tmp1, __tmp0: <FILL>, second: Any, msg: str="") :
        if isinstance(__tmp0, str) and isinstance(second, str):
            if __tmp0 != second:
                raise AssertionError("Actual and expected outputs do not match; showing diff.\n" +
                                     mdiff.diff_strings(__tmp0, second) + msg)
        else:
            super().assertEqual(__tmp0, second)

    def load_slack_message_conversion_tests(__tmp1) -> Dict[Any, Any]:
        test_fixtures = {}
        data_file = open(os.path.join(os.path.dirname(__file__), 'fixtures/slack_message_conversion.json'), 'r')
        data = ujson.loads('\n'.join(data_file.readlines()))
        for test in data['regular_tests']:
            test_fixtures[test['name']] = test

        return test_fixtures

    @slow("Aggregate of runs of individual slack message conversion tests")
    def test_message_conversion_fixtures(__tmp1) :
        format_tests = __tmp1.load_slack_message_conversion_tests()
        valid_keys = set(['name', "input", "conversion_output"])

        for name, test in format_tests.items():
            # Check that there aren't any unexpected keys as those are often typos
            __tmp1.assertEqual(len(set(test.keys()) - valid_keys), 0)
            slack_user_map = {}  # type: Dict[str, int]
            users = [{}]         # type: List[Dict[str, Any]]
            channel_map = {}     # type: Dict[str, Tuple[str, int]]
            converted = convert_to_zulip_markdown(test['input'], users, channel_map, slack_user_map)
            converted_text = converted[0]
            print("Running Slack Message Conversion test: %s" % (name,))
            __tmp1.assertEqual(converted_text, test['conversion_output'])

    def test_mentioned_data(__tmp1) :
        slack_user_map = {'U08RGD1RD': 540,
                          'U0CBK5KAT': 554,
                          'U09TYF5SK': 571}
        # For this test, only relevant keys are 'id', 'name', 'deleted'
        # and 'real_name'
        users = [{"id": "U0CBK5KAT",
                  "name": "aaron.anzalone",
                  "deleted": False,
                  "real_name": ""},
                 {"id": "U08RGD1RD",
                  "name": "john",
                  "deleted": False,
                  "real_name": "John Doe"},
                 {"id": "U09TYF5Sk",
                  "name": "Jane",
                  "deleted": True}]              # Deleted users don't have 'real_name' key in Slack
        channel_map = {'general': ('C5Z73A7RA', 137)}
        message = 'Hi <@U08RGD1RD|john>: How are you? <#C5Z73A7RA|general>'
        text, mentioned_users, has_link = convert_to_zulip_markdown(message, users, channel_map, slack_user_map)
        full_name = get_user_full_name(users[1])
        __tmp1.assertEqual(full_name, 'John Doe')
        __tmp1.assertEqual(get_user_full_name(users[2]), 'Jane')

        __tmp1.assertEqual(text, 'Hi @**%s**: How are you? #**general**' % (full_name))
        __tmp1.assertEqual(mentioned_users, [540])

        # multiple mentioning
        message = 'Hi <@U08RGD1RD|john>: How are you?<@U0CBK5KAT> asked.'
        text, mentioned_users, has_link = convert_to_zulip_markdown(message, users, channel_map, slack_user_map)
        __tmp1.assertEqual(text, 'Hi @**%s**: How are you?@**%s** asked.' %
                         ('John Doe', 'aaron.anzalone'))
        __tmp1.assertEqual(mentioned_users, [540, 554])

        # Check wrong mentioning
        message = 'Hi <@U08RGD1RD|jon>: How are you?'
        text, mentioned_users, has_link = convert_to_zulip_markdown(message, users, channel_map, slack_user_map)
        __tmp1.assertEqual(text, message)
        __tmp1.assertEqual(mentioned_users, [])

    def test_has_link(__tmp1) -> None:
        slack_user_map = {}  # type: Dict[str, int]

        message = '<http://journals.plos.org/plosone/article>'
        text, mentioned_users, has_link = convert_to_zulip_markdown(message, [], {}, slack_user_map)
        __tmp1.assertEqual(text, 'http://journals.plos.org/plosone/article')
        __tmp1.assertEqual(has_link, True)

        message = '<mailto:foo@foo.com>'
        text, mentioned_users, has_link = convert_to_zulip_markdown(message, [], {}, slack_user_map)
        __tmp1.assertEqual(text, 'mailto:foo@foo.com')
        __tmp1.assertEqual(has_link, True)

        message = 'random message'
        text, mentioned_users, has_link = convert_to_zulip_markdown(message, [], {}, slack_user_map)
        __tmp1.assertEqual(has_link, False)
