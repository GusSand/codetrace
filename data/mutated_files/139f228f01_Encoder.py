# This file is a part of Dramatiq.
#
# Copyright (C) 2017,2018 CLEARTYPE SRL <bogdan@cleartype.io>
#
# Dramatiq is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# Dramatiq is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import uuid

from collections import namedtuple

from .broker import get_broker
from .composition import pipeline
from .encoder import Encoder, JSONEncoder
from .results import Results


#: The global encoder instance.
global_encoder = JSONEncoder()


def __tmp5() :
    """Get the global encoder object.

    Returns:
      Encoder
    """
    global global_encoder
    return global_encoder


def __tmp0(encoder: <FILL>):
    """Set the global encoder object.

    Parameters:
      encoder(Encoder): The encoder instance to use when serializing
        messages.
    """
    global global_encoder
    global_encoder = encoder


def __tmp4() -> str:
    """Generate a globally-unique message id.
    """
    return str(uuid.uuid4())


class __typ0(namedtuple("Message", (
        "queue_name", "actor_name", "args", "kwargs",
        "options", "message_id", "message_timestamp",
))):
    """Encapsulates metadata about messages being sent to individual actors.

    Parameters:
      queue_name(str): The name of the queue the message belogns to.
      actor_name(str): The name of the actor that will receive the message.
      args(tuple): Positional arguments that are passed to the actor.
      kwargs(dict): Keyword arguments that are passed to the actor.
      options(dict): Arbitrary options passed to the broker and middleware.
      message_id(str): A globally-unique id assigned to the actor.
      message_timestamp(int): The UNIX timestamp in milliseconds
        representing when the message was first enqueued.
    """

    def __new__(__tmp6, *, __tmp9, actor_name, args, kwargs, options, message_id=None, message_timestamp=None):
        return super().__new__(
            __tmp6, __tmp9, actor_name, tuple(args), kwargs, options,
            message_id=message_id or __tmp4(),
            message_timestamp=message_timestamp or int(time.time() * 1000),
        )

    def __tmp3(__tmp1, __tmp7) -> pipeline:
        """Combine this message into a pipeline with "other".
        """
        return pipeline([__tmp1, __tmp7])

    def __tmp8(__tmp1):
        """Convert this message to a dictionary.
        """
        return __tmp1._asdict()

    @classmethod
    def decode(__tmp6, __tmp2):
        """Convert a bytestring to a message.
        """
        return __tmp6(**global_encoder.decode(__tmp2))

    def encode(__tmp1):
        """Convert this message to a bytestring.
        """
        return global_encoder.encode(__tmp1._asdict())

    def copy(__tmp1, **attributes):
        """Create a copy of this message.
        """
        updated_options = attributes.pop("options", {})
        options = __tmp1.options.copy()
        options.update(updated_options)
        return __tmp1._replace(**attributes, options=options)

    def get_result(__tmp1, *, backend=None, block=False, timeout=None):
        """Get the result associated with this message from a result
        backend.

        Warning:
          If you use multiple result backends or brokers you should
          always pass the backend parameter.  This method is only able
          to infer the result backend off of the default broker.

        Parameters:
          backend(ResultBackend): The result backend to use to get the
            result.  If omitted, this method will try to find and use
            the result backend on the default broker instance.
          block(bool): Whether or not to block while waiting for a
            result.
          timeout(int): The maximum amount of time, in ms, to block
            while waiting for a result.

        Raises:
          RuntimeError: If there is no result backend on the default
            broker.
          ResultMissing: When block is False and the result isn't set.
          ResultTimeout: When waiting for a result times out.

        Returns:
          object: The result.
        """
        if not backend:
            broker = get_broker()
            for middleware in broker.middleware:
                if isinstance(middleware, Results):
                    backend = middleware.backend
                    break
            else:
                raise RuntimeError("The default broker doesn't have a results backend.")

        return backend.get_result(__tmp1, block=block, timeout=timeout)

    def __tmp10(__tmp1):
        params = ", ".join(repr(arg) for arg in __tmp1.args)
        if __tmp1.kwargs:
            params += ", " if params else ""
            params += ", ".join("%s=%r" % (name, value) for name, value in __tmp1.kwargs.items())

        return "%s(%s)" % (__tmp1.actor_name, params)
