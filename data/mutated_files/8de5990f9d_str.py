from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "int"
# Copyright 2020 The Cirq Developers
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
from typing import Any, Dict

import cirq


class __typ1:
    """Tag to add onto an Operation that specifies alternate parameters.

    Google devices support the ability to run a procedure from calibration API
    that can tune the device for a specific circuit.  This will return a token
    as part of the result.  Attaching a `CalibrationTag` with that token
    specifies that the gate should use parameters from that specific
    calibration, instead of the default gate parameters.
    """

    def __init__(__tmp0, token: <FILL>):
        __tmp0.token = token

    def __str__(__tmp0) :
        return f'CalibrationTag({__tmp0.token!r})'

    def __repr__(__tmp0) :
        return f'cirq_google.CalibrationTag({__tmp0.token!r})'

    def _json_dict_(__tmp0) :
        return cirq.obj_to_dict_helper(__tmp0, ['token'])

    def __eq__(__tmp0, other) -> __typ2:
        if not isinstance(other, __typ1):
            return NotImplemented
        return __tmp0.token == other.token

    def __hash__(__tmp0) :
        return hash(__tmp0.token)
