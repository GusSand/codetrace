from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

from typing import Tuple, Optional, cast, Set

import abc
import os.path

from dev_tools import env_tools, shell_tools


class __typ1:
    """Output of a status check that passed, failed, or error'ed."""

    def __tmp4(
        __tmp0, check: 'Check', success, message: __typ0, unexpected_error: Optional[Exception]
    ) :
        __tmp0.check = check
        __tmp0.success = success
        __tmp0.message = message
        __tmp0.unexpected_error = unexpected_error

    def __tmp5(__tmp0):
        outcome = 'ERROR' if __tmp0.unexpected_error else 'pass' if __tmp0.success else 'FAIL'
        msg = __tmp0.unexpected_error if __tmp0.unexpected_error else __tmp0.message
        result = f'{outcome}: {__tmp0.check.context()} ({msg})'
        return shell_tools.highlight(result, shell_tools.GREEN if __tmp0.success else shell_tools.RED)


class Check(metaclass=abc.ABCMeta):
    """A status check that can performed in a python environment."""

    def __tmp4(__tmp0, *dependencies):
        __tmp0.dependencies = dependencies

    @abc.abstractmethod
    def command_line_switch(__tmp0) :
        """Used to identify this check from the command line."""

    @abc.abstractmethod
    def context(__tmp0) :
        """The name of this status check, as shown on github."""

    @abc.abstractmethod
    def perform_check(__tmp0, env, __tmp3: <FILL>) :
        """Evaluates the status check and returns a pass/fail with message.

        Args:
            env: Describes a prepared python 3 environment in which to run.
            verbose: When set, more progress output is produced.

        Returns:
            A tuple containing a pass/fail boolean and then a details message.
        """

    def __tmp2(__tmp0):
        return False

    def run(
        __tmp0, env, __tmp3, __tmp1
    ) :
        """Evaluates this check.

        Args:
            env: The prepared python environment to run the check in.
            verbose: When set, more progress output is produced.
            previous_failures: Checks that have already run and failed.

        Returns:
            A CheckResult instance.
        """

        # Skip if a dependency failed.
        if __tmp1.intersection(__tmp0.dependencies):
            print(
                shell_tools.highlight('Skipped ' + __tmp0.command_line_switch(), shell_tools.YELLOW)
            )
            return __typ1(__tmp0, False, 'Skipped due to dependency failing.', None)

        print(shell_tools.highlight('Running ' + __tmp0.command_line_switch(), shell_tools.GREEN))
        try:
            success, message = __tmp0.perform_check(env, __tmp3=__tmp3)
            result = __typ1(__tmp0, success, message, None)
        except Exception as ex:
            result = __typ1(__tmp0, False, 'Unexpected error.', ex)

        print(
            shell_tools.highlight(
                'Finished ' + __tmp0.command_line_switch(),
                shell_tools.GREEN if result.success else shell_tools.RED,
            )
        )
        if __tmp3:
            print(result)

        return result

    def pick_env_and_run_and_report(
        __tmp0, env, __tmp3: bool, __tmp1
    ) :
        """Evaluates this check in python 3 or 2.7, and reports to github.

        If the prepared environments are not linked to a github repository,
        with a known access token, reporting to github is skipped.

        Args:
            env: A prepared python 3 environment.
            verbose: When set, more progress output is produced.
            previous_failures: Checks that have already run and failed.

        Returns:
            A CheckResult instance.
        """
        env.report_status_to_github('pending', 'Running...', __tmp0.context())
        chosen_env = cast(env_tools.PreparedEnv, env)
        os.chdir(cast(__typ0, chosen_env.destination_directory))

        result = __tmp0.run(chosen_env, __tmp3, __tmp1)

        if result.unexpected_error is not None:
            env.report_status_to_github('error', 'Unexpected error.', __tmp0.context())
        else:
            env.report_status_to_github(
                'success' if result.success else 'failure', result.message, __tmp0.context()
            )

        return result
