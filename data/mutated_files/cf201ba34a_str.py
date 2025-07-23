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
class __typ0:
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

    def __post_init__(__tmp0):
        if not isinstance(__tmp0.name, str):
            raise ValueError("Measurement key name must be a valid string.")
        if MEASUREMENT_KEY_SEPARATOR in __tmp0.name:
            raise ValueError(
                f'Invalid key name: {__tmp0.name}\n{MEASUREMENT_KEY_SEPARATOR} is not allowed in '
                'MeasurementKey. If this is a nested key string, use '
                '`MeasurementKey.parse_serialized` for correct behavior.'
            )

    def replace(__tmp0, **changes) :
        """Returns a copy of this MeasurementKey with the specified changes."""
        return dataclasses.replace(__tmp0, **changes)

    def __eq__(__tmp0, other) :
        if isinstance(other, (__typ0, str)):
            return str(__tmp0) == str(other)
        return NotImplemented

    def __tmp1(__tmp0):
        if __tmp0.path:
            return f"cirq.MeasurementKey(path={__tmp0.path!r}, name='{__tmp0.name}')"
        else:
            return f"cirq.MeasurementKey(name='{__tmp0.name}')"

    def __str__(__tmp0):
        if __tmp0._str is None:
            object.__setattr__(
                __tmp0, '_str', MEASUREMENT_KEY_SEPARATOR.join(__tmp0.path + (__tmp0.name,))
            )
        return __tmp0._str

    def __hash__(__tmp0):
        if __tmp0._hash is None:
            object.__setattr__(__tmp0, '_hash', hash(str(__tmp0)))
        return __tmp0._hash

    def _json_dict_(__tmp0):
        return {
            'name': __tmp0.name,
            'path': __tmp0.path,
        }

    @classmethod
    def _from_json_dict_(
        cls,
        name,
        path,
        **kwargs,
    ):
        return cls(name=name, path=tuple(path))

    @classmethod
    def __tmp3(cls, key_str):
        """Parses the serialized string representation of `Measurementkey` into a `MeasurementKey`.

        This is the only way to construct a `MeasurementKey` from a nested string representation
        (where the path is joined to the key name by the `MEASUREMENT_KEY_SEPARATOR`)"""
        components = key_str.split(MEASUREMENT_KEY_SEPARATOR)
        return __typ0(name=components[-1], path=tuple(components[:-1]))

    def _with_key_path_(__tmp0, path):
        return __tmp0.replace(path=path)

    def _with_key_path_prefix_(__tmp0, __tmp2):
        return __tmp0._with_key_path_(path=__tmp2 + __tmp0.path)

    def __tmp4(__tmp0, *path_component: <FILL>):
        """Adds the input path component to the start of the path.

        Useful when constructing the path from inside to out (in case of nested subcircuits),
        recursively.
        """
        return __tmp0.replace(path=path_component + __tmp0.path)

    def _with_rescoped_keys_(
        __tmp0,
        path,
        bindable_keys: FrozenSet['MeasurementKey'],
    ):
        new_key = __tmp0.replace(path=path + __tmp0.path)
        if new_key in bindable_keys:
            raise ValueError(f'Conflicting measurement keys found: {new_key}')
        return new_key

    def _with_measurement_key_mapping_(__tmp0, key_map):
        if __tmp0.name not in key_map:
            return __tmp0
        return __tmp0.replace(name=key_map[__tmp0.name])
