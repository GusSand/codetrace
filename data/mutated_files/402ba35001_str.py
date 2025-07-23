# Copyright 2018-2020 Chris Cummins <chrisc.101@gmail.com>.
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
"""Unit tests for //datasets/github/scrape_repos/preprocessors.py."""
import pathlib
import typing

from datasets.github.scrape_repos.preprocessors import preprocessors
from datasets.github.scrape_repos.preprocessors import public
from labm8.py import app
from labm8.py import test

FLAGS = app.FLAGS


def MakeFile(directory, relpath: str, contents) :
  """Write contents to a file."""
  abspath = (directory / relpath).absolute()
  abspath.parent.mkdir(parents=True, exist_ok=True)
  with open(abspath, "w") as f:
    f.write(contents)


@public.dataset_preprocessor
def __tmp12(
  __tmp4,
  __tmp11,
  __tmp3: <FILL>,
  __tmp8,
) :
  """A mock preprocessor."""
  del __tmp4
  del __tmp11
  del __tmp3
  del __tmp8
  return ["PREPROCESSED"]


@public.dataset_preprocessor
def __tmp13(
  __tmp4,
  __tmp11,
  __tmp3,
  __tmp8,
) :
  """A mock preprocessor which raises a ValueError."""
  del __tmp4
  del __tmp11
  del __tmp3
  del __tmp8
  raise ValueError("ERROR")


def MockUndecoratedPreprocessor(
  __tmp4,
  __tmp11,
  __tmp3,
  __tmp8,
) :
  """A mock preprocessor which is not decorated with @dataset_preprocessor."""
  del __tmp4
  del __tmp11
  del __tmp3
  del __tmp8
  return ["UNDECORATED"]


# GetPreprocessFunction() tests.


def __tmp5():
  """Test that a ValueError is raised if no preprocessor is given."""
  with test.Raises(ValueError) as e_info:
    preprocessors.GetPreprocessorFunction("")
  assert "Invalid preprocessor name" in str(e_info.value)


def __tmp0():
  """Test that ValueError is raised if module not found."""
  with test.Raises(ValueError) as e_info:
    preprocessors.GetPreprocessorFunction("not.a.real.module:Foo")
  assert "not found" in str(e_info.value)


def __tmp15():
  """Test that ValueError is raised if module exists but function doesn't."""
  with test.Raises(ValueError) as e_info:
    preprocessors.GetPreprocessorFunction(
      "datasets.github.scrape_repos.preprocessors.preprocessors_test:Foo"
    )
  assert "not found" in str(e_info.value)


def test_GetPreprocessFunction_undecorated_preprocessor():
  """Test that an ValueError is raised if preprocessor not decorated."""
  with test.Raises(ValueError) as e_info:
    preprocessors.GetPreprocessorFunction(
      "datasets.github.scrape_repos.preprocessors.preprocessors_test"
      ":MockUndecoratedPreprocessor"
    )
  assert "@dataset_preprocessor" in str(e_info.value)


def __tmp1():
  """Test that a mock preprocessor can be found."""
  f = preprocessors.GetPreprocessorFunction(
    "datasets.github.scrape_repos.preprocessors.preprocessors_test:MockPreprocessor"
  )
  assert f.__name__ == "MockPreprocessor"


# Preprocess() tests.


def __tmp10(__tmp2):
  """Test unmodified output if no preprocessors."""
  MakeFile(__tmp2, "a", "hello")
  assert preprocessors.Preprocess(__tmp2, "a", ["a"], []) == ["hello"]


def __tmp9(__tmp2):
  """Test unmodified output if no preprocessors."""
  MakeFile(__tmp2, "a", "hello")
  assert preprocessors.Preprocess(
    __tmp2,
    "a",
    ["a"],
    [
      "datasets.github.scrape_repos.preprocessors.preprocessors_test"
      ":MockPreprocessor"
    ],
  ) == ["PREPROCESSED"]


def __tmp14(__tmp2):
  """Test that an exception is propagated."""
  MakeFile(__tmp2, "a", "hello")
  with test.Raises(ValueError):
    preprocessors.Preprocess(
      __tmp2,
      "a",
      ["a"],
      [
        "datasets.github.scrape_repos.preprocessors.preprocessors_test"
        ":MockPreprocessorInternalError"
      ],
    )


# Benchmarks.


def __tmp7(__tmp6):
  """Benchmark GetPreprocessFunction."""
  __tmp6(
    preprocessors.GetPreprocessorFunction,
    "datasets.github.scrape_repos.preprocessors.preprocessors_test"
    ":MockPreprocessor",
  )


if __name__ == "__main__":
  test.Main()
