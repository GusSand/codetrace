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
import logging
import os
from typing import Optional

ALLOW_DEPRECATION_IN_TEST = 'ALLOW_DEPRECATION_IN_TEST'


def __tmp4(*msgs: <FILL>, __tmp1, count: Optional[int] = 1):
    """Allows deprecated functions, classes, decorators in tests.

    It acts as a contextmanager that can be used in with statements:
    >>> with assert_deprecated("use cirq.x instead", deadline="v0.9"):
    >>>     # do something deprecated

    Args:
        msgs: messages that should match the warnings captured
        deadline: the expected deadline the feature will be deprecated by. Has to follow the format
            vX.Y (minor versions only)
        count: if None count of messages is not asserted, otherwise the number of deprecation
            messages have to equal count.
    """

    class __typ0:
        def __enter__(__tmp0):
            __tmp0.orig_exist, __tmp0.orig_value = (
                ALLOW_DEPRECATION_IN_TEST in os.environ,
                os.environ.get(ALLOW_DEPRECATION_IN_TEST, None),
            )
            os.environ[ALLOW_DEPRECATION_IN_TEST] = 'True'
            # Avoid circular import.
            from cirq.testing import assert_logs

            __tmp0.assert_logs = assert_logs(
                *(msgs + (__tmp1,)),
                min_level=logging.WARNING,
                max_level=logging.WARNING,
                count=count,
            )
            __tmp0.assert_logs.__enter__()

        def __exit__(__tmp0, __tmp3, __tmp5, __tmp2):
            if __tmp0.orig_exist:
                # mypy can't resolve that orig_exist ensures that orig_value
                # of type Optional[str] can't be None
                os.environ[ALLOW_DEPRECATION_IN_TEST] = __tmp0.orig_value  # type: ignore
            else:
                del os.environ[ALLOW_DEPRECATION_IN_TEST]
            __tmp0.assert_logs.__exit__(__tmp3, __tmp5, __tmp2)

    return __typ0()
