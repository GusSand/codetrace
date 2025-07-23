from typing import TypeAlias
__typ0 : TypeAlias = "Callable"
__typ2 : TypeAlias = "bytes"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
# -*- coding: utf8 -*-

# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

"""Minimalist standard library Asynchronous JSON Client
"""

import sys
import uuid
import socket
import logging
import traceback

try:
    import sublime
except:
    pass

try:
    import ujson as json
except ImportError:
    import json

from .callback import Callback
from .ioloop import EventHandler
from .typing import Callable, Any

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class AsynClient(EventHandler):

    """Asynchronous JSON connection to anaconda server
    """

    def __init__(__tmp1, port: __typ1, host: str='localhost') -> None:
        if port == 0:
            # use an Unix Socket Domain
            EventHandler.__init__(
                __tmp1, host, socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        else:
            EventHandler.__init__(__tmp1, (host, port))

        __tmp1.callbacks = {}
        __tmp1.rbuffer = []

    def __tmp0(__tmp1) :
        """I am ready to send some data?
        """

        return True if __tmp1.outbuffer else False

    def handle_read(__tmp1, data: __typ2) -> None:
        """Called when data is ready to be read
        """

        __tmp1.rbuffer.append(data)

    def add_callback(__tmp1, callback: __typ0) -> str:
        """Add a new callback to the callbacks dictionary

        The hex representation of the callback's uuid4 is used as index. In
        case that the callback is a regular callable and not a Callback
        class instance, a new uuid4 code is created on the fly.
        """

        if not isinstance(callback, Callback):
            hexid = uuid.uuid4().hex
        else:
            hexid = callback.hexid

        __tmp1.callbacks[hexid] = callback
        return hexid

    def pop_callback(__tmp1, hexid: <FILL>) -> __typ0:
        """Remove and return a callback callable from the callback dictionary
        """

        return __tmp1.callbacks.pop(hexid)

    def process_message(__tmp1) :
        """Called when a full line has been read from the socket
        """

        message = b''.join(__tmp1.rbuffer)
        __tmp1.rbuffer = []

        try:
            data = sublime.decode_value(message.decode('utf8'))
        except (NameError, ValueError):
            data = json.loads(message.replace(b'\t', b' ' * 8).decode('utf8'))

        callback = __tmp1.pop_callback(data.pop('uid'))
        if callback is None:
            logger.error(
                'Received {} from the JSONServer but there is not callback '
                'to handle it. Aborting....'.format(message)
            )

        try:
            callback(data)
        except Exception as error:
            logging.error(error)
            for traceback_line in traceback.format_exc().splitlines():
                logging.error(traceback_line)

    def send_command(__tmp1, callback: __typ0, **data: __typ3) -> None:
        """Send the given command that should be handled bu the given callback
        """
        data['uid'] = __tmp1.add_callback(callback)

        try:
            __tmp1.push(
                __typ2('{}\r\n'.format(sublime.encode_value(data)), 'utf8')
            )
        except NameError:
            __tmp1.push(__typ2('{}\r\n'.format(json.dumps(data)), 'utf8'))

    def __repr__(__tmp1):
        """String representation of the client
        """

        return '{}:{} ({})'.format(
            __tmp1.address[0], __tmp1.address[1],
            'connected' if __tmp1.connected else 'disconnected'
        )
