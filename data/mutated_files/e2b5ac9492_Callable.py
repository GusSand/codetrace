from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ2 : TypeAlias = "bytes"
__typ1 : TypeAlias = "str"
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
except ImportError:
    pass

try:
    import ujson as json
except ImportError:
    import json

from .callback import Callback
from .ioloop import EventHandler
from ._typing import Callable, Any

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)


class AsynClient(EventHandler):

    """Asynchronous JSON connection to anaconda server
    """

    def __init__(__tmp2, port, host: __typ1='localhost') :
        if port == 0:
            # use an Unix Socket Domain
            EventHandler.__init__(
                __tmp2, host, socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
        else:
            EventHandler.__init__(__tmp2, (host, port))

        __tmp2.callbacks = {}
        __tmp2.rbuffer = []

    def __tmp0(__tmp2) :
        """I am ready to send some data?
        """

        return True if __tmp2.outbuffer else False

    def handle_read(__tmp2, __tmp3: __typ2) :
        """Called when data is ready to be read
        """

        __tmp2.rbuffer.append(__tmp3)

    def add_callback(__tmp2, callback) -> __typ1:
        """Add a new callback to the callbacks dictionary

        The hex representation of the callback's uuid4 is used as index. In
        case that the callback is a regular callable and not a Callback
        class instance, a new uuid4 code is created on the fly.
        """

        if not isinstance(callback, Callback):
            hexid = uuid.uuid4().hex
        else:
            hexid = callback.hexid

        __tmp2.callbacks[hexid] = callback
        return hexid

    def pop_callback(__tmp2, hexid) -> Callable:
        """Remove and return a callback callable from the callback dictionary
        """

        return __tmp2.callbacks.pop(hexid)

    def __tmp4(__tmp2) :
        """Called when a full line has been read from the socket
        """

        message = b''.join(__tmp2.rbuffer)
        __tmp2.rbuffer = []

        try:
            __tmp3 = sublime.decode_value(message.decode('utf8'))
        except (NameError, ValueError):
            __tmp3 = json.loads(message.replace(b'\t', b' ' * 8).decode('utf8'))

        callback = __tmp2.pop_callback(__tmp3.pop('uid'))
        if callback is None:
            logger.error(
                'Received {} from the JSONServer but there is not callback '
                'to handle it. Aborting....'.format(message)
            )

        try:
            callback(__tmp3)
        except Exception as error:
            logging.error(error)
            for traceback_line in traceback.format_exc().splitlines():
                logging.error(traceback_line)

    def __tmp1(__tmp2, callback: <FILL>, **__tmp3: Any) :
        """Send the given command that should be handled bu the given callback
        """
        __tmp3['uid'] = __tmp2.add_callback(callback)

        try:
            __tmp2.push(
                __typ2('{}\r\n'.format(sublime.encode_value(__tmp3)), 'utf8')
            )
        except NameError:
            __tmp2.push(__typ2('{}\r\n'.format(json.dumps(__tmp3)), 'utf8'))

    def __tmp5(__tmp2):
        """String representation of the client
        """

        return '{}:{} ({})'.format(
            __tmp2.address[0], __tmp2.address[1],
            'connected' if __tmp2.connected else 'disconnected'
        )
