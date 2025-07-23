from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
__typ4 : TypeAlias = "bytes"
__typ3 : TypeAlias = "Any"
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


class __typ1(EventHandler):

    """Asynchronous JSON connection to anaconda server
    """

    def __init__(__tmp0, port: int, host: __typ0='localhost') :
        if port == 0:
            # use an Unix Socket Domain
            EventHandler.__init__(
                __tmp0, host, socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        else:
            EventHandler.__init__(__tmp0, (host, port))

        __tmp0.callbacks = {}
        __tmp0.rbuffer = []

    def ready_to_write(__tmp0) -> __typ2:
        """I am ready to send some data?
        """

        return True if __tmp0.outbuffer else False

    def handle_read(__tmp0, __tmp1) :
        """Called when data is ready to be read
        """

        __tmp0.rbuffer.append(__tmp1)

    def add_callback(__tmp0, callback: Callable) :
        """Add a new callback to the callbacks dictionary

        The hex representation of the callback's uuid4 is used as index. In
        case that the callback is a regular callable and not a Callback
        class instance, a new uuid4 code is created on the fly.
        """

        if not isinstance(callback, Callback):
            hexid = uuid.uuid4().hex
        else:
            hexid = callback.hexid

        __tmp0.callbacks[hexid] = callback
        return hexid

    def pop_callback(__tmp0, hexid: __typ0) -> Callable:
        """Remove and return a callback callable from the callback dictionary
        """

        return __tmp0.callbacks.pop(hexid)

    def process_message(__tmp0) -> None:
        """Called when a full line has been read from the socket
        """

        message = b''.join(__tmp0.rbuffer)
        __tmp0.rbuffer = []

        try:
            __tmp1 = sublime.decode_value(message.decode('utf8'))
        except (NameError, ValueError):
            __tmp1 = json.loads(message.replace(b'\t', b' ' * 8).decode('utf8'))

        callback = __tmp0.pop_callback(__tmp1.pop('uid'))
        if callback is None:
            logger.error(
                'Received {} from the JSONServer but there is not callback '
                'to handle it. Aborting....'.format(message)
            )

        try:
            callback(__tmp1)
        except Exception as error:
            logging.error(error)
            for traceback_line in traceback.format_exc().splitlines():
                logging.error(traceback_line)

    def send_command(__tmp0, callback: <FILL>, **__tmp1) -> None:
        """Send the given command that should be handled bu the given callback
        """
        __tmp1['uid'] = __tmp0.add_callback(callback)

        try:
            __tmp0.push(
                __typ4('{}\r\n'.format(sublime.encode_value(__tmp1)), 'utf8')
            )
        except NameError:
            __tmp0.push(__typ4('{}\r\n'.format(json.dumps(__tmp1)), 'utf8'))

    def __repr__(__tmp0):
        """String representation of the client
        """

        return '{}:{} ({})'.format(
            __tmp0.address[0], __tmp0.address[1],
            'connected' if __tmp0.connected else 'disconnected'
        )
