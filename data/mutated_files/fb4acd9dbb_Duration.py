from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A typed location in time that supports picosecond accuracy."""

from datetime import timedelta
from typing import Union, overload

from cirq.value.duration import Duration


class __typ3:
    """A location in time with picosecond accuracy.

    Supports affine operations against Duration."""

    def __init__(
        __tmp1, *, picos: Union[__typ1, __typ0] = 0, nanos: Union[__typ1, __typ0] = 0  # Forces keyword args.
    ) -> None:
        """Initializes a Timestamp with a time specified in ns and/or ps.

        The time is relative to some unspecified "time zero". If both picos and
        nanos are specified, their contributions away from zero are added.

        Args:
            picos: How many picoseconds away from time zero?
            nanos: How many nanoseconds away from time zero?
        """

        if picos and nanos:
            __tmp1._picos = picos + nanos * 1000
        else:
            # Try to preserve type information.
            __tmp1._picos = nanos * 1000 if nanos else picos

    def raw_picos(__tmp1) -> __typ0:
        """The timestamp's location in picoseconds from arbitrary time zero."""
        return __tmp1._picos

    def __add__(__tmp1, __tmp4) :
        if isinstance(__tmp4, timedelta):
            return __typ3(picos=__tmp1._picos + __tmp4.total_seconds() * 10 ** 12)
        if not isinstance(__tmp4, Duration):
            return NotImplemented
        return __typ3(picos=__tmp1._picos + __tmp4.total_picos())

    def __radd__(__tmp1, __tmp4) :
        return __tmp1.__add__(__tmp4)

    # pylint: disable=function-redefined
    @overload
    def __tmp2(__tmp1, __tmp4) -> Duration:
        pass

    @overload
    def __tmp2(__tmp1, __tmp4: <FILL>) :
        pass

    def __tmp2(__tmp1, __tmp4):
        if isinstance(__tmp4, Duration):
            return __typ3(picos=__tmp1._picos - __tmp4.total_picos())
        if isinstance(__tmp4, timedelta):
            return __typ3(picos=__tmp1._picos - __tmp4.total_seconds() * 10 ** 12)
        if isinstance(__tmp4, type(__tmp1)):
            return Duration(picos=__tmp1._picos - __tmp4._picos)
        return NotImplemented

    # pylint: enable=function-redefined

    def __tmp3(__tmp1, __tmp4):
        if not isinstance(__tmp4, type(__tmp1)):
            return NotImplemented
        return __tmp1._picos == __tmp4._picos

    def __ne__(__tmp1, __tmp4):
        return not __tmp1 == __tmp4

    def __gt__(__tmp1, __tmp4):
        if not isinstance(__tmp4, type(__tmp1)):
            return NotImplemented
        return __tmp1._picos > __tmp4._picos

    def __tmp0(__tmp1, __tmp4):
        if not isinstance(__tmp4, type(__tmp1)):
            return NotImplemented
        return __tmp1._picos < __tmp4._picos

    def __ge__(__tmp1, __tmp4):
        return not __tmp1 < __tmp4

    def __le__(__tmp1, __tmp4):
        return not __tmp1 > __tmp4

    def __hash__(__tmp1) :
        return hash((__typ3, __tmp1._picos))

    def __str__(__tmp1) -> __typ2:
        return f't={__tmp1._picos}'

    def __tmp5(__tmp1) :
        return f'cirq.Timestamp(picos={__tmp1._picos!r})'
