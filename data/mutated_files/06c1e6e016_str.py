# Copyright 2021 The Cirq Developers
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

from typing import Dict, FrozenSet, Optional, Tuple

import dataclasses

MEASUREMENT_KEY_SEPARATOR = ':'


@dataclasses.dataclass(frozen=True)
class MeasurementKey:
    """A class representing a Measurement Key.

    Wraps a string key. If you just want the string measurement key, simply call `str()` on this.

    Args:
        name: The string representation of the key.
        path: The path to this key in a circuit. In a multi-level circuit (one with repeated or
            nested subcircuits), we need to differentiate the keys that occur multiple times. The
            path is used to create such fully qualified unique measurement key based on where it
            occurs in the circuit. The path is outside-to-in, the outermost subcircuit identifier
            appears first in the tuple.
    """

    _hash: Optional[int] = dataclasses.field(default=None, init=False)
    _str: Optional[str] = dataclasses.field(default=None, init=False)

    name: str
    path: Tuple[str, ...] = dataclasses.field(default_factory=tuple)

    def __tmp5(__tmp1):
        if not isinstance(__tmp1.name, str):
            raise ValueError("Measurement key name must be a valid string.")
        if MEASUREMENT_KEY_SEPARATOR in __tmp1.name:
            raise ValueError(
                f'Invalid key name: {__tmp1.name}\n{MEASUREMENT_KEY_SEPARATOR} is not allowed in '
                'MeasurementKey. If this is a nested key string, use '
                '`MeasurementKey.parse_serialized` for correct behavior.'
            )

    def replace(__tmp1, **changes) -> 'MeasurementKey':
        """Returns a copy of this MeasurementKey with the specified changes."""
        return dataclasses.replace(__tmp1, **changes)

    def __tmp2(__tmp1, __tmp10) :
        if isinstance(__tmp10, (MeasurementKey, str)):
            return str(__tmp1) == str(__tmp10)
        return NotImplemented

    def __tmp11(__tmp1):
        if __tmp1.path:
            return f"cirq.MeasurementKey(path={__tmp1.path!r}, name='{__tmp1.name}')"
        else:
            return f"cirq.MeasurementKey(name='{__tmp1.name}')"

    def __str__(__tmp1):
        if __tmp1._str is None:
            object.__setattr__(
                __tmp1, '_str', MEASUREMENT_KEY_SEPARATOR.join(__tmp1.path + (__tmp1.name,))
            )
        return __tmp1._str

    def __tmp6(__tmp1):
        if __tmp1._hash is None:
            object.__setattr__(__tmp1, '_hash', hash(str(__tmp1)))
        return __tmp1._hash

    def __tmp14(__tmp1):
        return {
            'name': __tmp1.name,
            'path': __tmp1.path,
        }

    @classmethod
    def __tmp3(
        __tmp9,
        name,
        path,
        **kwargs,
    ):
        return __tmp9(name=name, path=tuple(path))

    @classmethod
    def __tmp13(__tmp9, __tmp7: <FILL>):
        """Parses the serialized string representation of `Measurementkey` into a `MeasurementKey`.

        This is the only way to construct a `MeasurementKey` from a nested string representation
        (where the path is joined to the key name by the `MEASUREMENT_KEY_SEPARATOR`)"""
        components = __tmp7.split(MEASUREMENT_KEY_SEPARATOR)
        return MeasurementKey(name=components[-1], path=tuple(components[:-1]))

    def _with_key_path_(__tmp1, path: Tuple[str, ...]):
        return __tmp1.replace(path=path)

    def __tmp15(__tmp1, prefix):
        return __tmp1._with_key_path_(path=prefix + __tmp1.path)

    def __tmp12(__tmp1, *path_component: str):
        """Adds the input path component to the start of the path.

        Useful when constructing the path from inside to out (in case of nested subcircuits),
        recursively.
        """
        return __tmp1.replace(path=path_component + __tmp1.path)

    def _with_rescoped_keys_(
        __tmp1,
        path: Tuple[str, ...],
        __tmp8: FrozenSet['MeasurementKey'],
    ):
        new_key = __tmp1.replace(path=path + __tmp1.path)
        if new_key in __tmp8:
            raise ValueError(f'Conflicting measurement keys found: {new_key}')
        return new_key

    def __tmp4(__tmp1, __tmp0):
        if __tmp1.name not in __tmp0:
            return __tmp1
        return __tmp1.replace(name=__tmp0[__tmp1.name])
