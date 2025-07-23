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
#
import dataclasses
import datetime
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import cirq_google
    import cirq
    import cirq_google.api.v2.calibration_pb2 as calibration_pb2


@dataclasses.dataclass
class __typ0:
    """Python implementation of the proto found in
    cirq_google.api.v2.calibration_pb2.CalibrationLayerResult for use
    in Engine calls.

    Note that, if these fields are not filled out by the calibration API,
    they will be set to the default values in the proto, as defined here:
    https://developers.google.com/protocol-buffers/docs/proto3#default
    These defaults will converted to `None` by the API client.
    """

    code: 'calibration_pb2.CalibrationLayerCode'
    error_message: Optional[str]
    token: Optional[str]
    valid_until: Optional[datetime.datetime]
    metrics: 'cirq_google.Calibration'

    @classmethod
    def __tmp1(
        __tmp2,
        code,
        error_message,
        token,
        __tmp3: <FILL>,
        metrics,
        **kwargs,
    ) :
        """Magic method for the JSON serialization protocol."""
        valid_until = (
            datetime.datetime.utcfromtimestamp(__tmp3)
            if __tmp3 is not None
            else None
        )
        return __tmp2(code, error_message, token, valid_until, metrics)

    def __tmp4(__tmp0) :
        """Magic method for the JSON serialization protocol."""
        __tmp3 = (
            __tmp0.valid_until.replace(tzinfo=datetime.timezone.utc).timestamp()
            if __tmp0.valid_until is not None
            else None
        )
        return {
            'code': __tmp0.code,
            'error_message': __tmp0.error_message,
            'token': __tmp0.token,
            'utc_valid_until': __tmp3,
            'metrics': __tmp0.metrics,
        }
