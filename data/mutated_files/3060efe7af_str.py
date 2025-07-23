from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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

import os
import sys
from typing import Optional, Iterable, Callable, cast

from dev_tools import shell_tools, git_env_tools
from dev_tools.github_repository import GithubRepository
from dev_tools.prepared_env import PreparedEnv


def get_unhidden_ungenerated_python_files(__tmp1: <FILL>) :
    """Iterates through relevant python files within the given directory.

    Args:
        directory: The top-level directory to explore.

    Yields:
        File paths.
    """
    for dirpath, dirnames, filenames in os.walk(__tmp1, topdown=True):
        if os.path.split(dirpath)[-1].startswith('.'):
            dirnames.clear()
            continue

        for filename in filenames:
            if filename.endswith('.py') and not filename.endswith('_pb2.py'):
                yield os.path.join(dirpath, filename)


def __tmp2(
    __tmp7, __tmp5: Iterable[str], __tmp3: str, __tmp6: __typ0
) -> None:
    """Creates a new virtual environment and then installs dependencies.

    Args:
        venv_path: Where to put the virtual environment's state.
        requirements_paths: Location of requirements files to -r install.
        python_path: The python binary to use.
        verbose: When set, more progress output is produced.
    """
    shell_tools.run_cmd(
        'virtualenv', None if __tmp6 else '--quiet', '-p', __tmp3, __tmp7, out=sys.stderr
    )
    pip_path = os.path.join(__tmp7, 'bin', 'pip')
    for req_path in __tmp5:
        shell_tools.run_cmd(
            pip_path, 'install', None if __tmp6 else '--quiet', '-r', req_path, out=sys.stderr
        )


def __tmp0(
    destination_directory,
    repository: GithubRepository,
    __tmp4,
    __tmp6: __typ0,
    env_name: str = '.test_virtualenv',
    __tmp3: str = sys.executable,
    commit_ids_known_callback: Callable[[PreparedEnv], None] = None,
) -> PreparedEnv:
    """Prepares a temporary test environment at the (existing empty) directory.

    Args:
        destination_directory: The location to put files. The caller is
            responsible for deleting the directory, whether or not this method
             succeeds or fails.
        repository: The github repository to download content from, if a pull
            request number is given.
        pull_request_number: If set, test content is fetched from github.
            Otherwise copies of local files are used.
        verbose: When set, more progress output is produced.
        env_name: The name to use for the virtual environment.
        python_path: Location of the python binary to use within the
            virtual environment.
        commit_ids_known_callback: A function to call when the actual commit id
            being tested is known, before the virtual environment is ready.

    Returns:
        Commit ids corresponding to content to test/compare.
    """
    # Fetch content.
    if __tmp4 is not None:
        env = git_env_tools.fetch_github_pull_request(
            destination_directory=destination_directory,
            repository=repository,
            __tmp4=__tmp4,
            __tmp6=__tmp6,
        )
    else:
        env = git_env_tools.fetch_local_files(
            destination_directory=destination_directory, __tmp6=__tmp6
        )

    if commit_ids_known_callback is not None:
        commit_ids_known_callback(env)

    # Create virtual environment.
    base_path = cast(str, env.destination_directory)
    env_path = os.path.join(base_path, env_name)
    req_path = os.path.join(base_path, 'requirements.txt')
    dev_req_path = os.path.join(base_path, 'dev_tools', 'requirements', 'deps', 'dev-tools.txt')
    contrib_req_path = os.path.join(base_path, 'cirq', 'contrib', 'requirements.txt')
    rev_paths = [req_path, dev_req_path, contrib_req_path]
    __tmp2(
        __tmp7=env_path, __tmp3=__tmp3, __tmp5=rev_paths, __tmp6=__tmp6
    )

    return PreparedEnv(
        github_repo=env.repository,
        actual_commit_id=env.actual_commit_id,
        compare_commit_id=env.compare_commit_id,
        destination_directory=env.destination_directory,
        virtual_env_path=env_path,
    )
