import mock
import os
from typing import Any, Dict
import ujson

from django.test import override_settings
from pika.exceptions import ConnectionClosed, AMQPConnectionError

from zerver.lib.queue import TornadoQueueClient, queue_json_publish, \
    get_queue_client, SimpleQueueClient
from zerver.lib.test_classes import ZulipTestCase

class __typ0(ZulipTestCase):
    @mock.patch('zerver.lib.queue.logging.getLogger', autospec=True)
    @mock.patch('zerver.lib.queue.ExceptionFreeTornadoConnection', autospec=True)
    def test_on_open_closed(__tmp3, mock_cxn: mock.MagicMock,
                            mock_get_logger: mock.MagicMock) -> None:
        connection = TornadoQueueClient()
        connection.connection.channel.side_effect = ConnectionClosed
        connection._on_open(mock.MagicMock())


class TestQueueImplementation(ZulipTestCase):
    @override_settings(USING_RABBITMQ=True)
    def test_queue_basics(__tmp3) -> None:
        queue_client = get_queue_client()
        queue_client.publish("test_suite", 'test_event')

        result = queue_client.drain_queue("test_suite")
        __tmp3.assertEqual(len(result), 1)
        __tmp3.assertEqual(result[0], b'test_event')

    @override_settings(USING_RABBITMQ=True)
    def test_queue_basics_json(__tmp3) :
        queue_json_publish("test_suite", {"event": "my_event"})

        queue_client = get_queue_client()
        result = queue_client.drain_queue("test_suite", json=True)
        __tmp3.assertEqual(len(result), 1)
        __tmp3.assertEqual(result[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def test_register_consumer(__tmp3) :
        output = []

        queue_client = get_queue_client()

        def __tmp4(event: Dict[str, Any]) -> None:
            output.append(event)
            queue_client.stop_consuming()

        queue_client.register_json_consumer("test_suite", __tmp4)
        queue_json_publish("test_suite", {"event": "my_event"})

        queue_client.start_consuming()

        __tmp3.assertEqual(len(output), 1)
        __tmp3.assertEqual(output[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def __tmp2(__tmp3) -> None:
        output = []
        count = 0

        queue_client = get_queue_client()

        def __tmp4(event) -> None:
            queue_client.stop_consuming()
            nonlocal count
            count += 1
            if count == 1:
                raise Exception("Make me nack!")
            output.append(event)

        queue_client.register_json_consumer("test_suite", __tmp4)
        queue_json_publish("test_suite", {"event": "my_event"})

        try:
            queue_client.start_consuming()
        except Exception:
            queue_client.register_json_consumer("test_suite", __tmp4)
            queue_client.start_consuming()

        # Confirm that we processed the event fully once
        __tmp3.assertEqual(count, 2)
        __tmp3.assertEqual(len(output), 1)
        __tmp3.assertEqual(output[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def test_queue_error_json(__tmp3) -> None:
        queue_client = get_queue_client()
        actual_publish = queue_client.publish

        __tmp3.counter = 0

        def throw_connection_error_once(__tmp0: <FILL>, *args: Any,
                                        **kwargs: Any) -> None:
            __tmp3.counter += 1
            if __tmp3.counter <= 1:
                raise AMQPConnectionError("test")
            actual_publish(*args, **kwargs)

        with mock.patch("zerver.lib.queue.SimpleQueueClient.publish",
                        throw_connection_error_once):
            queue_json_publish("test_suite", {"event": "my_event"})

        result = queue_client.drain_queue("test_suite", json=True)
        __tmp3.assertEqual(len(result), 1)
        __tmp3.assertEqual(result[0]['event'], 'my_event')

    @override_settings(USING_RABBITMQ=True)
    def __tmp1(__tmp3) -> None:
        queue_client = get_queue_client()
        queue_client.drain_queue("test_suite")
