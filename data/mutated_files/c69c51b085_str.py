# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase
from zerver.models import get_realm, get_user

class __typ0(WebhookTestCase):
    STREAM_NAME = 'wordpress'
    URL_TEMPLATE = "/api/v1/external/wordpress?api_key={api_key}&stream={stream}"
    FIXTURE_DIR_NAME = 'wordpress'

    def __tmp10(__tmp1) -> None:

        expected_topic = u"WordPress Post"
        expected_message = u"New post published.\n[New Blog Post](http://example.com\n)"

        __tmp1.send_and_test_stream_message('publish_post', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp2(__tmp1) -> None:

        expected_topic = u"WordPress Post"
        expected_message = u"New post published.\n[New Blog Post](http://example.com\n)"

        __tmp1.send_and_test_stream_message('publish_post_type_not_provided',
                                          expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp5(__tmp1) -> None:

        # Note: the fixture includes 'hook=publish_post' because it's always added by HookPress
        expected_topic = u"WordPress Notification"
        expected_message = u"New post published.\n" + "[New WordPress Post](WordPress Post URL)"

        __tmp1.send_and_test_stream_message('publish_post_no_data_provided',
                                          expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp9(__tmp1) -> None:

        expected_topic = u"WordPress Page"
        expected_message = u"New page published.\n" + "[New Blog Page](http://example.com\n)"

        __tmp1.send_and_test_stream_message('publish_page', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp4(__tmp1) :

        expected_topic = u"New Blog Users"
        expected_message = u"New blog user registered.\nName: test_user\nemail: test_user@example.com"

        __tmp1.send_and_test_stream_message('user_register', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp8(__tmp1) -> None:

        expected_topic = u"New Login"
        expected_message = u"User testuser logged in."

        __tmp1.send_and_test_stream_message('wp_login', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp6(__tmp1) -> None:

        # Mimic send_and_test_stream_message() to manually execute a negative test.
        # Otherwise its call to send_json_payload() would assert on the non-success
        # we are testing. The value of result is the error message the webhook should
        # return if no params are sent. The fixture for this test is an empty file.

        # subscribe to the target stream
        __tmp1.subscribe(__tmp1.test_user, __tmp1.STREAM_NAME)

        # post to the webhook url
        post_params = {'stream_name': __tmp1.STREAM_NAME,
                       'content_type': 'application/x-www-form-urlencoded'}
        result = __tmp1.client_post(__tmp1.url, 'unknown_action', **post_params)

        # check that we got the expected error message
        __tmp1.assert_json_error(result, "Unknown WordPress webhook action: WordPress Action")

    def __tmp3(__tmp1) :

        # Similar to unknown_action_no_data, except the fixture contains valid blog post
        # params but without the hook parameter. This should also return an error.

        __tmp1.subscribe(__tmp1.test_user, __tmp1.STREAM_NAME)
        post_params = {'stream_name': __tmp1.STREAM_NAME,
                       'content_type': 'application/x-www-form-urlencoded'}
        result = __tmp1.client_post(__tmp1.url, 'unknown_action', **post_params)

        __tmp1.assert_json_error(result, "Unknown WordPress webhook action: WordPress Action")

    def __tmp0(__tmp1, __tmp7: <FILL>) -> str:
        return __tmp1.webhook_fixture_data("wordpress", __tmp7, file_type="txt")
