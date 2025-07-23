# -*- coding: utf-8 -*-
import urllib
from typing import Optional

from zerver.lib.test_classes import WebhookTestCase

class __typ0(WebhookTestCase):
    STREAM_NAME = 'librato'
    URL_TEMPLATE = u"/api/v1/external/librato?api_key={api_key}&stream={stream}"
    FIXTURE_DIR_NAME = 'librato'
    IS_ATTACHMENT = False

    def __tmp1(__tmp2, __tmp6: <FILL>) -> str:
        if __tmp2.IS_ATTACHMENT:
            return __tmp2.webhook_fixture_data("librato", __tmp6, file_type='json')
        return urllib.parse.urlencode({'payload': __tmp2.webhook_fixture_data("librato", __tmp6, file_type='json')})

    def __tmp3(__tmp2) :
        expected_topic = 'Alert alert.name'
        expected_message = "Alert [alert_name](https://metrics.librato.com/alerts#/6294535) has triggered! [Reaction steps](http://www.google.pl)\n>Metric `librato.cpu.percent.idle`, sum was below 44 by 300s, recorded at 2016-03-31 09:11:42 UTC\n>Metric `librato.swap.swap.cached`, average was absent  by 300s, recorded at 2016-03-31 09:11:42 UTC\n>Metric `librato.swap.swap.cached`, derivative was above 9 by 300s, recorded at 2016-03-31 09:11:42 UTC"
        __tmp2.send_and_test_stream_message('alert', expected_topic, expected_message, content_type="application/x-www-form-urlencoded")

    def test_alert_message_with_custom_topic(__tmp2) :
        custom_topic = 'custom_name'
        __tmp2.url = __tmp2.build_webhook_url(topic=custom_topic)
        expected_message = "Alert [alert_name](https://metrics.librato.com/alerts#/6294535) has triggered! [Reaction steps](http://www.google.pl)\n>Metric `librato.cpu.percent.idle`, sum was below 44 by 300s, recorded at 2016-03-31 09:11:42 UTC\n>Metric `librato.swap.swap.cached`, average was absent  by 300s, recorded at 2016-03-31 09:11:42 UTC\n>Metric `librato.swap.swap.cached`, derivative was above 9 by 300s, recorded at 2016-03-31 09:11:42 UTC"
        __tmp2.send_and_test_stream_message('alert', custom_topic, expected_message, content_type="application/x-www-form-urlencoded")

    def __tmp0(__tmp2) :
        expected_message = "Alert [alert_name](https://metrics.librato.com/alerts#/6294535) has triggered! [Reaction steps](http://www.use.water.pl)\n>Metric `collectd.interface.eth0.if_octets.tx`, absolute_value was above 4 by 300s, recorded at 2016-04-11 20:40:14 UTC\n>Metric `collectd.load.load.longterm`, max was above 99, recorded at 2016-04-11 20:40:14 UTC\n>Metric `librato.swap.swap.cached`, average was absent  by 60s, recorded at 2016-04-11 20:40:14 UTC"
        expected_topic = 'Alert ToHighTemeprature'
        __tmp2.send_and_test_stream_message('three_conditions_alert', expected_topic, expected_message, content_type="application/x-www-form-urlencoded")

    def __tmp5(__tmp2) :
        expected_topic = 'Alert Alert_name'
        expected_message = "Alert [alert_name](https://metrics.librato.com/alerts#/6309313) has cleared at 2016-04-12 13:11:44 UTC!"
        __tmp2.send_and_test_stream_message('alert_cleared', expected_topic, expected_message, content_type="application/x-www-form-urlencoded")

    def __tmp4(__tmp2) :
        __tmp2.IS_ATTACHMENT = True
        expected_topic = 'Snapshots'
        expected_message = "**Hamlet** sent a [snapshot](http://snapshots.librato.com/chart/nr5l3n0c-82162.png) of [metric](https://metrics.librato.com/s/spaces/167315/explore/1731491?duration=72039&end_time=1460569409)"
        __tmp2.send_and_test_stream_message('snapshot', expected_topic, expected_message, content_type="application/x-www-form-urlencoded")
        __tmp2.IS_ATTACHMENT = False
