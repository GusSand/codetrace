from typing import TypeAlias
__typ1 : TypeAlias = "MagicMock"
# -*- coding: utf-8 -*-
from typing import Dict, Optional, Union

from mock import MagicMock, patch

from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'bitbucket'
    URL_TEMPLATE = "/api/v1/external/bitbucket?stream={stream}"
    FIXTURE_DIR_NAME = 'bitbucket'
    EXPECTED_TOPIC = u"Repository name"
    EXPECTED_TOPIC_BRANCH_EVENTS = u"Repository name / master"

    def __tmp3(__tmp0) :
        __tmp4 = 'push'
        __tmp0.url = __tmp0.build_webhook_url(payload=__tmp0.get_body(__tmp4))
        commit_info = u'* c ([25f93d2](https://bitbucket.org/kolaszek/repository-name/commits/25f93d22b719e2d678a7ad5ee0ef0d1fcdf39c12))'
        expected_message = u"kolaszek pushed 1 commit to branch master.\n\n{}".format(commit_info)
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, __tmp4, __tmp0.EXPECTED_TOPIC_BRANCH_EVENTS,
                                expected_message)

    def test_bitbucket_on_push_event_filtered_by_branches(__tmp0) -> None:
        __tmp4 = 'push'
        __tmp0.url = __tmp0.build_webhook_url(payload=__tmp0.get_body(__tmp4),
                                          branches='master,development')
        commit_info = u'* c ([25f93d2](https://bitbucket.org/kolaszek/repository-name/commits/25f93d22b719e2d678a7ad5ee0ef0d1fcdf39c12))'
        expected_message = u"kolaszek pushed 1 commit to branch master.\n\n{}".format(commit_info)
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, __tmp4, __tmp0.EXPECTED_TOPIC_BRANCH_EVENTS,
                                expected_message)

    def test_bitbucket_on_push_commits_above_limit_event(__tmp0) -> None:
        __tmp4 = 'push_commits_above_limit'
        __tmp0.url = __tmp0.build_webhook_url(payload=__tmp0.get_body(__tmp4))
        commit_info = u'* c ([25f93d2](https://bitbucket.org/kolaszek/repository-name/commits/25f93d22b719e2d678a7ad5ee0ef0d1fcdf39c12))\n'
        expected_message = u"kolaszek pushed 50 commits to branch master.\n\n{}[and 30 more commit(s)]".format(commit_info * 20)
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, __tmp4, __tmp0.EXPECTED_TOPIC_BRANCH_EVENTS,
                                expected_message)

    def __tmp2(__tmp0) -> None:
        __tmp4 = 'push_commits_above_limit'
        __tmp0.url = __tmp0.build_webhook_url(payload=__tmp0.get_body(__tmp4),
                                          branches='master,development')
        commit_info = u'* c ([25f93d2](https://bitbucket.org/kolaszek/repository-name/commits/25f93d22b719e2d678a7ad5ee0ef0d1fcdf39c12))\n'
        expected_message = u"kolaszek pushed 50 commits to branch master.\n\n{}[and 30 more commit(s)]".format(commit_info * 20)
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, __tmp4, __tmp0.EXPECTED_TOPIC_BRANCH_EVENTS,
                                expected_message)

    def __tmp5(__tmp0) :
        __tmp4 = 'force_push'
        __tmp0.url = __tmp0.build_webhook_url(payload=__tmp0.get_body(__tmp4))
        expected_message = u"kolaszek [force pushed](https://bitbucket.org/kolaszek/repository-name)"
        __tmp0.api_stream_message(__tmp0.TEST_USER_EMAIL, __tmp4, __tmp0.EXPECTED_TOPIC,
                                expected_message)

    @patch('zerver.webhooks.bitbucket.view.check_send_webhook_message')
    def test_bitbucket_on_push_event_filtered_by_branches_ignore(__tmp0, __tmp1) :
        __tmp4 = 'push'
        payload = __tmp0.get_body(__tmp4)
        __tmp0.url = __tmp0.build_webhook_url(payload=payload,
                                          branches='changes,development')
        result = __tmp0.api_post(__tmp0.TEST_USER_EMAIL, __tmp0.url, payload, content_type="application/json,")
        __tmp0.assertFalse(__tmp1.called)
        __tmp0.assert_json_success(result)

    @patch('zerver.webhooks.bitbucket.view.check_send_webhook_message')
    def test_bitbucket_push_commits_above_limit_filtered_by_branches_ignore(
            __tmp0, __tmp1) :
        __tmp4 = 'push_commits_above_limit'
        payload = __tmp0.get_body(__tmp4)
        __tmp0.url = __tmp0.build_webhook_url(payload=payload,
                                          branches='changes,development')
        result = __tmp0.api_post(__tmp0.TEST_USER_EMAIL, __tmp0.url, payload, content_type="application/json,")
        __tmp0.assertFalse(__tmp1.called)
        __tmp0.assert_json_success(result)

    def get_body(__tmp0, __tmp4: <FILL>) -> Union[str, Dict[str, str]]:
        return __tmp0.webhook_fixture_data(__tmp0.FIXTURE_DIR_NAME, __tmp4)
