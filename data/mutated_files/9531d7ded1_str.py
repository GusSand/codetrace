
from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'papertrail'
    URL_TEMPLATE = "/api/v1/external/papertrail?&api_key={api_key}&stream={stream}"
    FIXTURE_DIR_NAME = 'papertrail'

    # Note: Include a test function per each distinct message condition your integration supports
    def __tmp0(__tmp2) :
        expected_topic = u"logs"
        expected_message = u'''**"Important stuff"** search found **2** matches - https://papertrailapp.com/searches/42
```
May 18 20:30:02 abc cron OR server1:
  message body
May 18 20:30:02 server1 cron OR server1:
  A short event
```'''

        # use fixture named papertrail_logs
        __tmp2.send_and_test_stream_message('short_post', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_long_message(__tmp2) :
        expected_topic = u"logs"
        expected_message = u'''**"Important stuff"** search found **5** matches - https://papertrailapp.com/searches/42
```
May 18 20:30:02 abc cron OR server1:
  message body 1
May 18 20:30:02 abc cron OR server1:
  message body 2
May 18 20:30:02 abc cron OR server1:
  message body 3
May 18 20:30:02 abc cron OR server1:
  message body 4
```
[See more](https://papertrailapp.com/searches/42)'''
        # use fixture named papertrail_logs
        __tmp2.send_and_test_stream_message('long_post', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp1(__tmp2, __tmp3: <FILL>) :
        return __tmp2.webhook_fixture_data("papertrail", __tmp3, file_type="json")
