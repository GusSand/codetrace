# -*- coding: utf-8 -*-

from django.test import TestCase

from zerver.lib.test_classes import WebhookTestCase
from zerver.webhooks.appfollow.view import convert_markdown

class AppFollowHookTests(WebhookTestCase):
    STREAM_NAME = 'appfollow'
    URL_TEMPLATE = u"/api/v1/external/appfollow?stream={stream}&api_key={api_key}"

    def __tmp4(__tmp2) :
        expected_topic = "Webhook integration was successful."
        expected_message = u"""Webhook integration was successful.
Test User / Acme (Google Play)"""
        __tmp2.send_and_test_stream_message('sample', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def test_reviews(__tmp2) :
        expected_topic = "Acme - Group chat"
        expected_message = u"""Acme - Group chat
App Store, Acme Technologies, Inc.
★★★★★ United States
**Great for Information Management**
Acme enables me to manage the flow of information quite well. I only wish I could create and edit my Acme Post files in the iOS app.
*by* **Mr RESOLUTIONARY** *for v3.9*
[Permalink](http://appfollow.io/permalink) · [Add tag](http://watch.appfollow.io/add_tag)"""
        __tmp2.send_and_test_stream_message('review', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")

    def __tmp3(__tmp2) :
        # This temporary patch of URL_TEMPLATE is code smell but required due to the way
        # WebhookTestCase is built.
        original_url_template = __tmp2.URL_TEMPLATE
        __tmp2.URL_TEMPLATE = original_url_template + "&topic=foo"
        __tmp2.url = __tmp2.build_webhook_url()
        expected_topic = "foo"
        expected_message = u"""Acme - Group chat
App Store, Acme Technologies, Inc.
★★★★★ United States
**Great for Information Management**
Acme enables me to manage the flow of information quite well. I only wish I could create and edit my Acme Post files in the iOS app.
*by* **Mr RESOLUTIONARY** *for v3.9*
[Permalink](http://appfollow.io/permalink) · [Add tag](http://watch.appfollow.io/add_tag)"""
        __tmp2.send_and_test_stream_message('review', expected_topic, expected_message,
                                          content_type="application/x-www-form-urlencoded")
        __tmp2.URL_TEMPLATE = original_url_template

    def __tmp0(__tmp2, fixture_name: <FILL>) :
        return __tmp2.webhook_fixture_data("appfollow", fixture_name, file_type="json")

class ConvertMarkdownTest(TestCase):
    def test_convert_bold(__tmp2) :
        __tmp2.assertEqual(convert_markdown("*test message*"), "**test message**")

    def __tmp1(__tmp2) :
        __tmp2.assertEqual(convert_markdown("_test message_"), "*test message*")
        __tmp2.assertEqual(convert_markdown("_  spaced message _"), "  *spaced message* ")

    def test_convert_strikethrough(__tmp2) :
        __tmp2.assertEqual(convert_markdown("~test message~"), "~~test message~~")
