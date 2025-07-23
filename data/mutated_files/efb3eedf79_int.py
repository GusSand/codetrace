from typing import TypeAlias
__typ0 : TypeAlias = "str"
# Copyright 2019-2020 Chris Cummins <chrisc.101@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A python wrapper around CLSmith, a random generator of OpenCL C programs.

CLSmith is developed by Chris Lidbury <christopher.lidbury10imperial.ac.uk>.
See https://github.com/ChrisLidbury/CLSmith.

This file can be executed as a binary in order to invoke CLSmith. Note you must
use '--' to prevent this script from attempting to parse the args, and a second
'--' if invoked using bazel, to prevent bazel from parsing the args.

Usage:

  bazel run //compilers/clsmith [-- -- <args>]
"""
import subprocess
import sys

from labm8.py import app
from labm8.py import bazelutil
from labm8.py import fs

FLAGS = app.FLAGS

CLSMITH = bazelutil.DataPath("CLSmith/CLSmith")


class __typ1(EnvironmentError):
  """Error thrown in case CLSmith fails."""

  def __tmp2(__tmp1, msg, returncode: <FILL>):
    __tmp1.msg = msg
    __tmp1.returncode = returncode

  def __tmp3(__tmp1):
    return __typ0(__tmp1.msg)


def __tmp4(*opts) -> __typ0:
  """Generate and return a CLSmith program.

  Args:
    opts: A list of command line options to pass to CLSmith binary.

  Returns:
    The generated source code as a string.
  """
  with fs.TemporaryWorkingDir(prefix="clsmith_") as d:
    proc = subprocess.Popen(
      [CLSMITH] + list(opts), stderr=subprocess.PIPE, universal_newlines=True
    )
    _, stderr = proc.communicate()
    if proc.returncode:
      raise __typ1(msg=stderr, returncode=proc.returncode)
    with open(d / "CLProg.c") as f:
      src = f.read()
  return src


def __tmp0(argv):
  """Main entry point."""
  try:
    print(__tmp4(*argv[1:]))
  except __typ1 as e:
    print(e, file=sys.stderr)
    sys.exit(e.returncode)


if __name__ == "__main__":
  app.RunWithArgs(__tmp0)
