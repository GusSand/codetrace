
import ujson

from django.http import HttpResponse
from mock import patch
from typing import Any, Dict

from zerver.lib.test_classes import ZulipTestCase
from zerver.lib.stream_topic import StreamTopicTarget

from zerver.models import (
    get_realm,
    get_stream,
    get_stream_recipient,
    get_user,
    Recipient,
    UserProfile,
)

from zerver.lib.topic_mutes import (
    add_topic_mute,
    get_topic_mutes,
    topic_is_muted,
)

class __typ0(ZulipTestCase):
    def __tmp0(__tmp1) -> None:
        hamlet = __tmp1.example_user('hamlet')
        cordelia  = __tmp1.example_user('cordelia')
        realm = hamlet.realm
        stream = get_stream(u'Verona', realm)
        recipient = get_stream_recipient(stream.id)
        topic_name = 'teST topic'

        stream_topic_target = StreamTopicTarget(
            stream_id=stream.id,
            topic_name=topic_name,
        )

        user_ids = stream_topic_target.user_ids_muting_topic()
        __tmp1.assertEqual(user_ids, set())

        def __tmp4(user: <FILL>) -> None:
            add_topic_mute(
                user_profile=user,
                stream_id=stream.id,
                recipient_id=recipient.id,
                topic_name='test TOPIC',
            )

        __tmp4(hamlet)
        user_ids = stream_topic_target.user_ids_muting_topic()
        __tmp1.assertEqual(user_ids, {hamlet.id})

        __tmp4(cordelia)
        user_ids = stream_topic_target.user_ids_muting_topic()
        __tmp1.assertEqual(user_ids, {hamlet.id, cordelia.id})

    def test_add_muted_topic(__tmp1) :
        email = __tmp1.example_email('hamlet')
        __tmp1.login(email)

        url = '/api/v1/users/me/subscriptions/muted_topics'
        data = {'stream': 'Verona', 'topic': 'Verona3', 'op': 'add'}
        result = __tmp1.api_patch(email, url, data)
        __tmp1.assert_json_success(result)

        user = __tmp1.example_user('hamlet')
        __tmp1.assertIn([u'Verona', u'Verona3'], get_topic_mutes(user))

        stream = get_stream(u'Verona', user.realm)
        __tmp1.assertTrue(topic_is_muted(user, stream.id, 'Verona3'))
        __tmp1.assertTrue(topic_is_muted(user, stream.id, 'verona3'))

    def __tmp2(__tmp1) -> None:
        __tmp1.user_profile = __tmp1.example_user('hamlet')
        email = __tmp1.user_profile.email
        __tmp1.login(email)

        realm = __tmp1.user_profile.realm
        stream = get_stream(u'Verona', realm)
        recipient = get_stream_recipient(stream.id)
        add_topic_mute(
            user_profile=__tmp1.user_profile,
            stream_id=stream.id,
            recipient_id=recipient.id,
            topic_name=u'Verona3',
        )

        url = '/api/v1/users/me/subscriptions/muted_topics'
        data = {'stream': 'Verona', 'topic': 'vERONA3', 'op': 'remove'}
        result = __tmp1.api_patch(email, url, data)

        __tmp1.assert_json_success(result)
        user = __tmp1.example_user('hamlet')
        __tmp1.assertNotIn([[u'Verona', u'Verona3']], get_topic_mutes(user))

    def __tmp3(__tmp1) :
        __tmp1.user_profile = __tmp1.example_user('hamlet')
        email = __tmp1.user_profile.email
        __tmp1.login(email)

        realm = __tmp1.user_profile.realm
        stream = get_stream(u'Verona', realm)
        recipient = get_stream_recipient(stream.id)
        add_topic_mute(
            user_profile=__tmp1.user_profile,
            stream_id=stream.id,
            recipient_id=recipient.id,
            topic_name=u'Verona3',
        )

        url = '/api/v1/users/me/subscriptions/muted_topics'
        data = {'stream': 'Verona', 'topic': 'Verona3', 'op': 'add'}
        result = __tmp1.api_patch(email, url, data)
        __tmp1.assert_json_error(result, "Topic already muted")

    def __tmp5(__tmp1) :
        __tmp1.user_profile = __tmp1.example_user('hamlet')
        email = __tmp1.user_profile.email
        __tmp1.login(email)

        url = '/api/v1/users/me/subscriptions/muted_topics'
        data = {'stream': 'BOGUS', 'topic': 'Verona3', 'op': 'remove'}
        result = __tmp1.api_patch(email, url, data)
        __tmp1.assert_json_error(result, "Topic is not muted")

        data = {'stream': 'Verona', 'topic': 'BOGUS', 'op': 'remove'}
        result = __tmp1.api_patch(email, url, data)
        __tmp1.assert_json_error(result, "Topic is not muted")
