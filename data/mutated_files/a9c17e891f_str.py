from typing import TypeAlias
__typ0 : TypeAlias = "int"
# Copyright (c) 2016-2020 Chris Cummins.
#
# clgen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# clgen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with clgen.  If not, see <https://www.gnu.org/licenses/>.
"""Common preprocessor passes."""
from deeplearning.clgen import errors
from deeplearning.clgen.preprocessors import public
from labm8.py import app

FLAGS = app.FLAGS


def __tmp5(__tmp1: <FILL>, __tmp0: __typ0) -> str:
  """Private implementation of minimum number of lines.

  Args:
    text: The source to verify the line count of.

  Returns:
    src: The unmodified input src.

  Raises:
    NoCodeException: If src is less than min_line_count long.
  """
  if len(__tmp1.strip().split("\n")) < __tmp0:
    raise errors.NoCodeException
  return __tmp1


@public.clgen_preprocessor
def __tmp2(__tmp1: str) -> str:
  """Check that file contains a minimum number of lines.

  Args:
    text: The source to verify the line count of.

  Returns:
    src: The unmodified input src.

  Raises:
    NoCodeException: If src is less than min_line_count long.
  """
  return __tmp5(__tmp1, 3)


@public.clgen_preprocessor
def __tmp3(__tmp1: str) -> str:
  """A preprocessor pass which removes duplicate empty lines.

  Args:
    text: The text to preprocess.

  Returns:
    The input text, where duplicate empty lines have been removed.
  """
  last_line = None
  lines = []
  for line in __tmp1.split("\n"):
    if line.strip() or last_line:
      lines.append(line)
    last_line = line.rstrip()
  return "\n".join(lines)


@public.clgen_preprocessor
def __tmp4(__tmp1) -> str:
  """A preprocessor pass which strips trailing whitespace from all lines.

  Whitespace at the end of each line is removed, as is any trailing whitespace
  at the end of the input.

  Args:
    text: The text to preprocess.

  Returns:
    The input text, with trailing whitespace removed.
  """
  return "\n".join(l.rstrip() for l in __tmp1.split("\n")).rstrip()
