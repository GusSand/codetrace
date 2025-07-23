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

import abc
import json
import pickle
import typing


#: Represents the contents of a Message object as a dict.
__typ0 = typing.Dict[str, typing.Any]


class __typ1(abc.ABC):
    """Base class for message encoders.
    """

    @abc.abstractmethod
    def encode(__tmp0, __tmp1) :  # pragma: no cover
        """Convert message metadata into a bytestring.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def decode(__tmp0, __tmp1) :  # pragma: no cover
        """Convert a bytestring into message metadata.
        """
        raise NotImplementedError


class JSONEncoder(__typ1):
    """Encodes messages as JSON.  This is the default encoder.
    """

    def encode(__tmp0, __tmp1) :
        return json.dumps(__tmp1, separators=(",", ":")).encode("utf-8")

    def decode(__tmp0, __tmp1: <FILL>) :
        return json.loads(__tmp1.decode("utf-8"))


class PickleEncoder(__typ1):
    """Pickles messages.

    Warning:
      This encoder is not secure against maliciously-constructed data.
      Use it at your own risk.
    """

    encode = pickle.dumps
    decode = pickle.loads
