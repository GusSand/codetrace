import mock
import os
from typing import Any, Dict
import ujson

from django.test import override_settings
from pika.exceptions import ConnectionClosed, AMQPConnectionError

from zerver.lib.queue import TornadoQueueClient, queue_json_publish, \
    get_queue_client, SimpleQueueClient
from zerver.lib.test_classes import ZulipTestCase

class TestTornadoQueueClient(ZulipTestCase):
    @mock.patch('zerver.lib.queue.logging.getLogger', autospec=True)
    @mock.patch('zerver.lib.queue.ExceptionFreeTornadoConnection', autospec=True)
    def test_on_open_closed(__tmp1, mock_cxn,
                            mock_get_logger) :
        connection = TornadoQueueClient()
        connection.connection.channel.side_effect = ConnectionClosed
        connection._on_open(mock.MagicMock())


class TestQueueImplementation(ZulipTestCase):
    @override_settings(USING_RABBITMQ=True)
    def __tmp0(__tmp1) :
        queue_client = get_queue_client()
        queue_client.publish("test_suite", 'test_event')

        result = queue_client.drain_queue("test_suite")
        __tmp1.assertEqual(len(result), 1)
        __tmp1.assertEqual(result[0], b'test_event')

    @override_settings(USING_RABBITMQ=True)
    def __tmp2(__tmp1) :
        queue_json_publish("test_suite", {"event": "my_event"})

        queue_client = get_queue_client()
        result = queue_client.drain_queue("test_suite", json=True)
        __tmp1.assertEqual(len(result), 1)
        __tmp1.assertEqual(result[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def test_register_consumer(__tmp1) :
        output = []

        queue_client = get_queue_client()

        def collect(event) :
            output.append(event)
            queue_client.stop_consuming()

        queue_client.register_json_consumer("test_suite", collect)
        queue_json_publish("test_suite", {"event": "my_event"})

        queue_client.start_consuming()

        __tmp1.assertEqual(len(output), 1)
        __tmp1.assertEqual(output[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def test_register_consumer_nack(__tmp1) :
        output = []
        count = 0

        queue_client = get_queue_client()

        def collect(event) :
            queue_client.stop_consuming()
            nonlocal count
            count += 1
            if count == 1:
                raise Exception("Make me nack!")
            output.append(event)

        queue_client.register_json_consumer("test_suite", collect)
        queue_json_publish("test_suite", {"event": "my_event"})

        try:
            queue_client.start_consuming()
        except Exception:
            queue_client.register_json_consumer("test_suite", collect)
            queue_client.start_consuming()

        # Confirm that we processed the event fully once
        __tmp1.assertEqual(count, 2)
        __tmp1.assertEqual(len(output), 1)
        __tmp1.assertEqual(output[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def test_queue_error_json(__tmp1) :
        queue_client = get_queue_client()
        actual_publish = queue_client.publish

        __tmp1.counter = 0

        def throw_connection_error_once(self_obj, *args: <FILL>,
                                        **kwargs) :
            __tmp1.counter += 1
            if __tmp1.counter <= 1:
                raise AMQPConnectionError("test")
            actual_publish(*args, **kwargs)

        with mock.patch("zerver.lib.queue.SimpleQueueClient.publish",
                        throw_connection_error_once):
            queue_json_publish("test_suite", {"event": "my_event"})

        result = queue_client.drain_queue("test_suite", json=True)
        __tmp1.assertEqual(len(result), 1)
        __tmp1.assertEqual(result[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def tearDown(__tmp1) :
        queue_client = get_queue_client()
        queue_client.drain_queue("test_suite")
