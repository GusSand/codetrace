# -*- coding: utf-8 -*-
from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'statuspage-test'
    URL_TEMPLATE = u"/api/v1/external/statuspage?api_key={api_key}&stream={stream}"

    def test_statuspage_incident(__tmp1) :
        expected_topic = u"Database query delays: All Systems Operational"
        expected_message = u"**Database query delays** \n * State: **identified** \n \
* Description: We just encountered that database queries are timing out resulting in inconvenience \
to our end users...we'll do quick fix latest by tommorow !!!"
        __tmp1.send_and_test_stream_message('incident_created',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp3(__tmp1) :
        expected_topic = u"Database query delays: All Systems Operational"
        expected_message = u"**Database query delays** \n * State: **resolved** \n \
* Description: The database issue is resolved."
        __tmp1.send_and_test_stream_message('incident_update',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp4(__tmp1) -> None:
        expected_topic = u"Database component: Service Under Maintenance"
        expected_message = u"**Database component** has changed status \
from **operational** to **under_maintenance**"
        __tmp1.send_and_test_stream_message('component_status_update',
                                          expected_topic,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp0(__tmp1, __tmp2: <FILL>) :
        return __tmp1.webhook_fixture_data("statuspage", __tmp2, file_type="json")
