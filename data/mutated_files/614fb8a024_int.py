# Copyright 2019 The Cirq Developers
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

from typing import List, Iterable, Any, Union, Optional, overload


def __tmp7(__tmp4) :
    """Returns the big-endian integer specified by the given bits.

    Args:
        bits: Descending bits of the integer, with the 1s bit at the end.

    Returns:
        The integer.

    Examples:

        >>> cirq.big_endian_bits_to_int([0, 1])
        1

        >>> cirq.big_endian_bits_to_int([1, 0])
        2

        >>> cirq.big_endian_bits_to_int([0, 1, 0])
        2

        >>> cirq.big_endian_bits_to_int([1, 0, 0, 1, 0])
        18
    """
    result = 0
    for e in __tmp4:
        result <<= 1
        if e:
            result |= 1
    return result


def __tmp5(__tmp0: int, *, __tmp1) :
    """Returns the big-endian bits of an integer.

    Args:
        val: The integer to get bits from. This integer is permitted to be
            larger than `2**bit_count` (in which case the high bits of the
            result are dropped) or to be negative (in which case the bits come
            from the 2s complement signed representation).
        bit_count: The number of desired bits in the result.

    Returns:
        The bits.

    Examples:
        >>> cirq.big_endian_int_to_bits(19, bit_count=8)
        [0, 0, 0, 1, 0, 0, 1, 1]

        >>> cirq.big_endian_int_to_bits(19, bit_count=4)
        [0, 0, 1, 1]

        >>> cirq.big_endian_int_to_bits(-3, bit_count=4)
        [1, 1, 0, 1]
    """
    return [(__tmp0 >> i) & 1 for i in range(__tmp1)[::-1]]


def big_endian_digits_to_int(digits: Iterable[int], *, __tmp2) :
    """Returns the big-endian integer specified by the given digits and base.

    Args:
        digits: Digits of the integer, with the least significant digit at the
            end.
        base: The base, or list of per-digit bases, to use when combining the
            digits into an integer. When a list of bases is specified, the last
            entry in the list is the base for the last entry of the digits list
            (i.e. the least significant digit). That is to say, the bases are
            also specified in big endian order.

    Returns:
        The integer.

    Raises:
        ValueError:
            One of the digits is out of range for its base.
            The base was specified per-digit (as a list) but the length of the
                bases list is different from the number of digits.

    Examples:

        >>> cirq.big_endian_digits_to_int([0, 1], base=10)
        1

        >>> cirq.big_endian_digits_to_int([1, 0], base=10)
        10

        >>> cirq.big_endian_digits_to_int([1, 2, 3], base=[2, 3, 4])
        23
    """
    digits = tuple(digits)
    __tmp2 = (__tmp2,) * len(digits) if isinstance(__tmp2, int) else tuple(__tmp2)
    if len(digits) != len(__tmp2):
        raise ValueError('len(digits) != len(base)')

    result = 0
    for d, b in zip(digits, __tmp2):
        if not (0 <= d < b):
            raise ValueError(f'Out of range digit. Digit: {d!r}, base: {b!r}')
        result *= b
        result += d
    return result


# pylint: disable=function-redefined
@overload
def __tmp3(__tmp0: <FILL>, *, __tmp6: int, __tmp2: int) -> List[int]:
    pass


@overload
def __tmp3(__tmp0: int, *, __tmp2) -> List[int]:
    pass


def __tmp3(
    __tmp0, *, __tmp6: Optional[int] = None, __tmp2
) :
    """Separates an integer into big-endian digits.

    Args:
        val: The integer to get digits from. Must be non-negative and less than
            the maximum representable value, given the specified base(s) and
            digit count.
        base: The base, or list of per-digit bases, to separate `val` into. When
             a list of bases is specified, the last entry in the list is the
             base for the last entry of the result (i.e. the least significant
             digit). That is to say, the bases are also specified in big endian
             order.
        digit_count: The length of the desired result.

    Returns:
        The list of digits.

    Raises:
        ValueError:
            Unknown digit count. The `base` was specified as an integer and a
                `digit_count` was not provided.
            Inconsistent digit count. The `base` was specified as a per-digit
                list, and `digit_count` was also provided, but they disagree.

    Examples:
        >>> cirq.big_endian_int_to_digits(11, digit_count=4, base=10)
        [0, 0, 1, 1]

        >>> cirq.big_endian_int_to_digits(11, base=[2, 3, 4])
        [0, 2, 3]
    """
    if isinstance(__tmp2, int):
        if __tmp6 is None:
            raise ValueError('No digit count. Provide `digit_count` when base is an int.')
        __tmp2 = (__tmp2,) * __tmp6
    else:
        __tmp2 = tuple(__tmp2)
        if __tmp6 is None:
            __tmp6 = len(__tmp2)

    if len(__tmp2) != __tmp6:
        raise ValueError('Inconsistent digit count. len(base) != digit_count')

    result = []
    for b in reversed(__tmp2):
        result.append(__tmp0 % b)
        __tmp0 //= b

    if __tmp0:
        raise ValueError(
            'Out of range. '
            'Extracted digits {!r} but the long division process '
            'left behind {!r} instead of 0.'.format(result, __tmp0)
        )

    return result[::-1]


# pylint: enable=function-redefined
