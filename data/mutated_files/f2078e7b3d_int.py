from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def __tmp3(__tmp2, min_line_count: <FILL>) -> __typ0:
  """Private implementation of minimum number of lines.

  Args:
    text: The source to verify the line count of.

  Returns:
    src: The unmodified input src.

  Raises:
    NoCodeException: If src is less than min_line_count long.
  """
  if len(__tmp2.strip().split("\n")) < min_line_count:
    raise errors.NoCodeException
  return __tmp2


@public.clgen_preprocessor
def __tmp0(__tmp2) :
  """Check that file contains a minimum number of lines.

  Args:
    text: The source to verify the line count of.

  Returns:
    src: The unmodified input src.

  Raises:
    NoCodeException: If src is less than min_line_count long.
  """
  return __tmp3(__tmp2, 3)


@public.clgen_preprocessor
def __tmp1(__tmp2) -> __typ0:
  """A preprocessor pass which removes duplicate empty lines.

  Args:
    text: The text to preprocess.

  Returns:
    The input text, where duplicate empty lines have been removed.
  """
  last_line = None
  lines = []
  for line in __tmp2.split("\n"):
    if line.strip() or last_line:
      lines.append(line)
    last_line = line.rstrip()
  return "\n".join(lines)


@public.clgen_preprocessor
def StripTrailingWhitespace(__tmp2) :
  """A preprocessor pass which strips trailing whitespace from all lines.

  Whitespace at the end of each line is removed, as is any trailing whitespace
  at the end of the input.

  Args:
    text: The text to preprocess.

  Returns:
    The input text, with trailing whitespace removed.
  """
  return "\n".join(l.rstrip() for l in __tmp2.split("\n")).rstrip()
