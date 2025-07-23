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
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Tuple

import pytest
from filelock import FileLock

from dev_tools import shell_tools
from dev_tools.env_tools import create_virtual_env


def __tmp1(__tmp8):
    __tmp8.addinivalue_line("markers", "slow: mark tests as slow")


def __tmp4(__tmp8, items):
    keywordexpr = __tmp8.option.keyword
    markexpr = __tmp8.option.markexpr
    if keywordexpr or markexpr:
        return  # let pytest handle this

    skip_slow_marker = pytest.mark.skip(reason='slow marker not selected')
    for item in items:
        if 'slow' in item.keywords:
            item.add_marker(skip_slow_marker)


@pytest.fixture(scope="session")
def __tmp2(__tmp9, __tmp10):
    """Fixture to allow tests to run in a clean virtual env.

    It de-duplicates installation of base packages. Assuming `virtualenv-clone` exists on the PATH,
    it creates first a prototype environment and then clones for each new request the same env.
    This fixture is safe to use with parallel execution, i.e. pytest-xdist. The workers synchronize
    via a file lock, the first worker will (re)create the prototype environment, the others will
    reuse it via cloning.

    A group of tests that share the same base environment is identified by a name, `env_dir`,
    which will become the directory within the temporary directory to hold the virtualenv.

    Usage:

    >>> def test_something_in_clean_env(cloned_env):
            # base_env will point to a pathlib.Path containing the virtual env which will
            # have quimb, jinja and whatever reqs.txt contained.
            base_env = cloned_env("some_tests", "quimb", "jinja", "-r", "reqs.txt")

            # To install new packages (that are potentially different for each test instance)
            # just run pip install from the virtual env
            subprocess.run(f"{base_env}/bin/pip install something".split(" "))
            ...

    Returns:
        a function to create the cloned base environment with signature
        `def base_env_creator(env_dir: str, *pip_install_args: str) -> Path`.
        Use `env_dir` to specify the directory name per shared base packages.
        Use `pip_install_args` varargs to pass arguments to `pip install`, these
        can be requirements files, e.g. `'-r','dev_tools/.../something.txt'` or
        actual packages as well, e.g.`'quimb'`.
    """
    __tmp0 = None

    def __tmp7(__tmp11, *__tmp6) :
        """The function to create a cloned base environment."""
        # get/create a temp directory shared by all workers
        base_temp_path = Path(tempfile.gettempdir()) / "cirq-pytest"
        os.makedirs(name=base_temp_path, exist_ok=True)
        nonlocal __tmp0
        __tmp0 = base_temp_path / __tmp11
        with FileLock(str(__tmp0) + ".lock"):
            if _check_for_reuse_or_recreate(__tmp0):
                print(f"Pytest worker [{__tmp10}] is reusing {__tmp0} for '{__tmp11}'.")
            else:
                print(f"Pytest worker [{__tmp10}] is creating {__tmp0} for '{__tmp11}'.")
                __tmp3(__tmp0, __tmp6)

        clone_dir = base_temp_path / str(uuid.uuid4())
        shell_tools.run_cmd("virtualenv-clone", str(__tmp0), str(clone_dir))
        return clone_dir

    def _check_for_reuse_or_recreate(__tmp5):
        reuse = False
        if __tmp5.is_dir() and (__tmp5 / "testrun.uid").is_file():
            uid = open(__tmp5 / "testrun.uid").readlines()[0]
            # if the dir is from this test session, let's reuse it
            if uid == __tmp9:
                reuse = True
            else:
                # if we have a dir from a previous test session, recreate it
                shutil.rmtree(__tmp5)
        return reuse

    def __tmp3(__tmp0: <FILL>, __tmp6):
        try:
            create_virtual_env(str(__tmp0), [], sys.executable, True)
            with open(__tmp0 / "testrun.uid", mode="w") as f:
                f.write(__tmp9)
            if __tmp6:
                shell_tools.run_cmd(f"{__tmp0}/bin/pip", "install", *__tmp6)
        except BaseException as ex:
            # cleanup on failure
            if __tmp0.is_dir():
                print(f"Removing {__tmp0}, due to error: {ex}")
                shutil.rmtree(__tmp0)
            raise

    return __tmp7
