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

"""Progress and logging facilities for the quantum runtime."""

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import cirq_google as cg


class _WorkflowLogger(abc.ABC):
    """Implementers of this class can provide logging and progress information
    for execution loops."""

    def initialize(__tmp1):
        """Initialization logic at the start of an execution loop."""

    def __tmp2(
        __tmp1, __tmp3: 'cg.ExecutableResult', __tmp4: 'cg.SharedRuntimeInfo'
    ):
        """Consume executable results as they are completed.

        Args:
            exe_result: The completed `cg.ExecutableResult`.
            shared_rt_info: A reference to the `cg.SharedRuntimeInfo` for this
                execution at this point.
        """

    def __tmp0(__tmp1):
        """Finalization logic at the end of an execution loop."""


class _PrintLogger(_WorkflowLogger):
    def __init__(__tmp1, n_total: <FILL>):
        __tmp1.n_total = n_total
        __tmp1.i = 0

    def initialize(__tmp1):
        """Write a newline at the start of an execution loop."""
        print()

    def __tmp2(
        __tmp1, __tmp3: 'cg.ExecutableResult', __tmp4: 'cg.SharedRuntimeInfo'
    ):
        """Print a simple count of completed executables."""
        print(f'\r{__tmp1.i + 1} / {__tmp1.n_total}', end='', flush=True)
        __tmp1.i += 1

    def __tmp0(__tmp1):
        """Write a newline at the end of an execution loop."""
        print()
