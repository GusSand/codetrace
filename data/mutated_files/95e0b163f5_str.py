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


def MakeFile(__tmp4, __tmp0, __tmp9) :
  """Write contents to a file."""
  abspath = (__tmp4 / __tmp0).absolute()
  abspath.parent.mkdir(parents=True, exist_ok=True)
  with open(abspath, "w") as f:
    f.write(__tmp9)


@public.dataset_preprocessor
def MockPreprocessor(
  __tmp2: pathlib.Path,
  __tmp8,
  __tmp3,
  __tmp7,
) -> typing.List[str]:
  """A mock preprocessor."""
  del __tmp2
  del __tmp8
  del __tmp3
  del __tmp7
  return ["PREPROCESSED"]


@public.dataset_preprocessor
def __tmp11(
  __tmp2,
  __tmp8: str,
  __tmp3,
  __tmp7: typing.List[str],
) -> typing.List[str]:
  """A mock preprocessor which raises a ValueError."""
  del __tmp2
  del __tmp8
  del __tmp3
  del __tmp7
  raise ValueError("ERROR")


def __tmp10(
  __tmp2,
  __tmp8: <FILL>,
  __tmp3,
  __tmp7,
) -> typing.List[str]:
  """A mock preprocessor which is not decorated with @dataset_preprocessor."""
  del __tmp2
  del __tmp8
  del __tmp3
  del __tmp7
  return ["UNDECORATED"]


# GetPreprocessFunction() tests.


def test_GetPreprocessFunction_empty_string():
  """Test that a ValueError is raised if no preprocessor is given."""
  with test.Raises(ValueError) as e_info:
    preprocessors.GetPreprocessorFunction("")
  assert "Invalid preprocessor name" in str(e_info.value)


def __tmp5():
  """Test that ValueError is raised if module not found."""
  with test.Raises(ValueError) as e_info:
    preprocessors.GetPreprocessorFunction("not.a.real.module:Foo")
  assert "not found" in str(e_info.value)


def test_GetPreprocessFunction_missing_function():
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


def test_GetPreprocessFunction_mock_preprocessor():
  """Test that a mock preprocessor can be found."""
  f = preprocessors.GetPreprocessorFunction(
    "datasets.github.scrape_repos.preprocessors.preprocessors_test:MockPreprocessor"
  )
  assert f.__name__ == "MockPreprocessor"


# Preprocess() tests.


def __tmp13(__tmp1):
  """Test unmodified output if no preprocessors."""
  MakeFile(__tmp1, "a", "hello")
  assert preprocessors.Preprocess(__tmp1, "a", ["a"], []) == ["hello"]


def __tmp6(__tmp1):
  """Test unmodified output if no preprocessors."""
  MakeFile(__tmp1, "a", "hello")
  assert preprocessors.Preprocess(
    __tmp1,
    "a",
    ["a"],
    [
      "datasets.github.scrape_repos.preprocessors.preprocessors_test"
      ":MockPreprocessor"
    ],
  ) == ["PREPROCESSED"]


def __tmp12(__tmp1):
  """Test that an exception is propagated."""
  MakeFile(__tmp1, "a", "hello")
  with test.Raises(ValueError):
    preprocessors.Preprocess(
      __tmp1,
      "a",
      ["a"],
      [
        "datasets.github.scrape_repos.preprocessors.preprocessors_test"
        ":MockPreprocessorInternalError"
      ],
    )


# Benchmarks.


def test_benchmark_GetPreprocessFunction_mock(benchmark):
  """Benchmark GetPreprocessFunction."""
  benchmark(
    preprocessors.GetPreprocessorFunction,
    "datasets.github.scrape_repos.preprocessors.preprocessors_test"
    ":MockPreprocessor",
  )


if __name__ == "__main__":
  test.Main()
