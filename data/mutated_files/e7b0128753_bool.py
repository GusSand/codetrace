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
"""Unit tests for //datasets/github:api."""
import os
import pathlib

from datasets.github import api
from datasets.github.testing.requires_access_token import requires_access_token
from labm8.py import app
from labm8.py import fs
from labm8.py import test

FLAGS = app.FLAGS


def __tmp16(__tmp1):
  with test.Raises(FileNotFoundError):
    api.ReadGithubAccessTokenPath(__tmp1 / "not_a_file.txt")


def __tmp2(__tmp1):
  path = __tmp1 / "access_token.txt"
  path.touch()
  with test.Raises(api.BadCredentials) as e_ctx:
    api.ReadGithubAccessTokenPath(path)

  assert str(e_ctx.value) == "Access token not found in file"


def __tmp5(
  __tmp1,
):
  path = __tmp1 / "access_token.txt"
  path.touch()
  os.chmod(path, 0o000)
  with test.Raises(api.BadCredentials) as e_ctx:
    api.ReadGithubAccessTokenPath(path)

  assert str(e_ctx.value) == "Cannot read file"


def __tmp11(__tmp1,):
  path = __tmp1 / "access_token.txt"
  path.mkdir()
  with test.Raises(api.BadCredentials) as e_ctx:
    api.ReadGithubAccessTokenPath(path)

  assert str(e_ctx.value) == "File is a directory"


def __tmp6(__tmp1: pathlib.Path,):
  path = __tmp1 / "access_token.txt"
  fs.Write(path, "1234".encode("utf-8"))

  assert api.ReadGithubAccessTokenPath(path) == "1234"


def __tmp15(
  __tmp1,
):
  with test.TemporaryEnv() as env:
    env["GITHUB_ACCESS_TOKEN"] = "1234"
    source, token = api.GetDefaultGithubAccessToken()

  assert source == "$GITHUB_ACCESS_TOKEN"
  assert token == "1234"


def __tmp7(
  __tmp1,
):
  path = __tmp1 / "access_token_path.txt"
  fs.Write(path, "1234".encode("utf-8"))
  with test.TemporaryEnv() as env:
    env["GITHUB_ACCESS_TOKEN_PATH"] = str(path)
    source, token = api.GetDefaultGithubAccessToken()

  assert source == f"$GITHUB_ACCESS_TOKEN_PATH={path}"
  assert token == "1234"


def __tmp4(
  __tmp1,
):
  path = __tmp1 / "access_token_path.txt"
  path.touch()
  with test.TemporaryEnv() as env:
    env["GITHUB_ACCESS_TOKEN_PATH"] = str(path)
    with test.Raises(api.BadCredentials) as e_ctx:
      api.GetDefaultGithubAccessToken()

  assert str(e_ctx.value) == (
    f"Invalid credentials file $GITHUB_ACCESS_TOKEN_PATH={path}: "
    "Access token not found in file"
  )


def __tmp3(
  __tmp1,
):
  FLAGS.unparse_flags()
  FLAGS(["argv[0]", "--github_access_token", "1234"])

  source, token = api.GetDefaultGithubAccessToken()

  assert source == "--github_access_token"
  assert token == "1234"


def __tmp13(
  __tmp1,
):
  path = __tmp1 / "access_token_path.txt"
  fs.Write(path, "1234".encode("utf-8"))

  FLAGS.unparse_flags()
  FLAGS(["argv[0]", "--github_access_token_path", str(path)])

  source, token = api.GetDefaultGithubAccessToken()

  assert source == f"--github_access_token_path={path}"
  assert token == "1234"


def __tmp8(
  __tmp1: pathlib.Path,
):
  path = __tmp1 / "access_token_path.txt"
  path.touch()

  FLAGS.unparse_flags()
  FLAGS(["argv[0]", "--github_access_token_path", str(path)])

  with test.Raises(api.BadCredentials) as e_ctx:
    api.GetDefaultGithubAccessToken()

  assert str(e_ctx.value) == (
    f"Invalid credentials file --github_access_token_path={path}: "
    "Access token not found in file"
  )


def test_GetDefaultGithubAccessToken_from_extra_paths(__tmp1: pathlib.Path):
  path = __tmp1 / "access_token_path.txt"
  fs.Write(path, "1234".encode("utf-8"))

  source, token = api.GetDefaultGithubAccessToken(
    extra_access_token_paths=[path]
  )

  assert source == str(path)
  assert token == "1234"


@requires_access_token
def __tmp12():
  github = api.GetDefaultGithubConnection()
  github.get_user("ChrisCummins")


@requires_access_token
def __tmp9():
  github = api.GetDefaultGithubConnectionOrDie()
  github.get_user("ChrisCummins")


@requires_access_token
@test.Parametrize(
  "shallow", (False, True), names=("deep_clone", "shallow_clone")
)
def __tmp10(__tmp1, __tmp14: <FILL>):
  github = api.GetDefaultGithubConnectionOrDie()
  repo = github.get_repo("ChrisCummins/empty_repository_for_testing")
  clone_path = __tmp1 / "repo"

  # Note forced https because test runner may not have access to SSH
  # keys in ~/.ssh.
  assert (
    api.CloneRepo(repo, __tmp1 / "repo", __tmp14=__tmp14, force_https=True)
    == clone_path
  )
  assert (clone_path / "HelloWorld.java").is_file()


@requires_access_token
@test.Parametrize(
  "shallow", (False, True), names=("deep_clone", "shallow_clone")
)
def __tmp0(__tmp1, __tmp14):
  github = api.GetDefaultGithubConnectionOrDie()
  repo = github.get_repo("ChrisCummins/not_a_real_repo")

  with test.Raises(FileNotFoundError):
    api.CloneRepo(repo, __tmp1, __tmp14=__tmp14)


if __name__ == "__main__":
  test.Main()
