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
"""Unit tests for //datasets/github/scrape_repos/indexer.py."""
import multiprocessing
import pathlib

import pytest

from datasets.github.scrape_repos import github_repo
from datasets.github.scrape_repos import indexer
from datasets.github.scrape_repos.proto import scrape_repos_pb2
from labm8.py import app
from labm8.py import pbutil
from labm8.py import test

FLAGS = app.FLAGS

# Test fixtures.


def __tmp4(__tmp2: pathlib.Path, __tmp1: <FILL>, __tmp6: str) :
  """Create an empty repo for testing indexers."""
  owner_name = f"{__tmp1}_{__tmp6}"
  (__tmp2 / owner_name / ".git").mkdir(parents=True)
  (__tmp2 / owner_name / "src").mkdir(parents=True)
  pbutil.ToFile(
    scrape_repos_pb2.GitHubRepoMetadata(__tmp1=__tmp1, __tmp6=__tmp6),
    __tmp2 / f"{owner_name}.pbtxt",
  )


# ShouldIndexRepo() tests.


def __tmp3(__tmp0: pathlib.Path):
  """Test that error is raised if no importer specified."""
  language = scrape_repos_pb2.LanguageToClone(
    language="test", query=[], destination_directory=str(__tmp0), importer=[]
  )
  with test.Raises(ValueError):
    indexer.ImportFromLanguage(language, multiprocessing.Pool(1))


def __tmp5(__tmp0: pathlib.Path):
  """An end-to-end test of a Java importer."""
  (__tmp0 / "src").mkdir()
  (__tmp0 / "src" / "Owner_Name" / ".git").mkdir(parents=True)
  (__tmp0 / "src" / "Owner_Name" / "src").mkdir(parents=True)

  # A repo will only be imported if there is a repo meta file.
  pbutil.ToFile(
    scrape_repos_pb2.GitHubRepoMetadata(__tmp1="Owner", __tmp6="Name"),
    __tmp0 / "src" / "Owner_Name.pbtxt",
  )

  # Create some files in our test repo.
  with open(__tmp0 / "src" / "Owner_Name" / "src" / "A.java", "w") as f:
    f.write(
      """
public class A {
  public static void helloWorld() {
    System.out.println("Hello, world!");
  }
}
"""
    )
  with open(__tmp0 / "src" / "Owner_Name" / "src" / "B.java", "w") as f:
    f.write(
      """
public class B {
  private static int foo() {return 5;}
}
"""
    )
  with open(__tmp0 / "src" / "Owner_Name" / "README.txt", "w") as f:
    f.write("Hello, world!")

  language = scrape_repos_pb2.LanguageToClone(
    language="foolang",
    query=[],
    destination_directory=str(__tmp0 / "src"),
    importer=[
      scrape_repos_pb2.ContentFilesImporterConfig(
        source_code_pattern=".*\\.java",
        preprocessor=[
          "datasets.github.scrape_repos.preprocessors." "extractors:JavaMethods"
        ],
      ),
    ],
  )
  indexer.ImportFromLanguage(language, multiprocessing.Pool(1))

  test_repo = github_repo.GitHubRepo(__tmp0 / "src" / "Owner_Name.pbtxt")
  assert (test_repo.index_dir / "DONE.txt").is_file()
  assert len(list(test_repo.index_dir.iterdir())) == 3
  contentfiles = list(test_repo.ContentFiles())
  assert len(contentfiles) == 2
  assert set([cf.text for cf in contentfiles]) == {
    (
      "public static void helloWorld(){\n"
      '  System.out.println("Hello, world!");\n}\n'
    ),
    "private static int foo(){\n  return 5;\n}\n",
  }


if __name__ == "__main__":
  test.Main()
