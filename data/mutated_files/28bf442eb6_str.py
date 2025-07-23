from typing import TypeAlias
__typ0 : TypeAlias = "bytes"
__typ1 : TypeAlias = "bool"
"""Utilities for verifying git integrity."""

# Used also from setup.py, so don't pull in anything additional here (like mypy or typing):
import os
import pipes
import subprocess
import sys

MYPY = False
if MYPY:
    from typing import Iterator


def is_git_repo(dir: str) -> __typ1:
    """Is the given directory version-controlled with git?"""
    return os.path.exists(os.path.join(dir, ".git"))


def __tmp10() -> __typ1:
    """Can we run the git executable?"""
    try:
        subprocess.check_output(["git", "--help"])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False


def __tmp2(dir: str) -> "Iterator[str]":
    """Return a list of all git top-level submodules in a given directory."""
    # It would be nicer to do
    # "git submodule foreach 'echo MODULE $name $path $sha1 $toplevel'"
    # but that wouldn't work on Windows.
    output = subprocess.check_output(["git", "submodule", "status"], cwd=dir)
    # "<status><sha1> name desc"
    # status='-': not initialized
    # status='+': changed
    # status='u': merge conflicts
    # status=' ': up-to-date
    for line in output.splitlines():
        # Skip the status indicator, as it could be a space can confuse the split.
        line = line[1:]
        __tmp11 = line.split(b" ")[1]
        yield __tmp11.decode(sys.getfilesystemencoding())


def __tmp9(dir: str) -> __typ0:
    """Get the SHA-1 of the HEAD of a git repository."""
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dir).strip()


def __tmp6(dir: str, __tmp0: str) -> __typ0:
    """Get the SHA-1 a submodule is supposed to have."""
    output = subprocess.check_output(["git", "ls-files", "-s", __tmp0], cwd=dir).strip()
    # E.g.: "160000 e4a7edb949e0b920b16f61aeeb19fc3d328f3012 0       typeshed"
    return output.split()[1]


def __tmp1(dir: str) -> __typ1:
    """Check whether a git repository has uncommitted changes."""
    output = subprocess.check_output(["git", "status", "-uno", "--porcelain"], cwd=dir)
    return output.strip() != b""


def __tmp4(dir: str) -> __typ1:
    """Check whether a git repository has untracked files."""
    output = subprocess.check_output(["git", "clean", "--dry-run", "-d"], cwd=dir)
    return output.strip() != b""


def warn_no_git_executable() -> None:
    print("Warning: Couldn't check git integrity. "
          "git executable not in path.", file=sys.stderr)


def warn_dirty(dir: str) -> None:
    print("Warning: git module '{}' has uncommitted changes.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and commit or reset your changes", file=sys.stderr)


def warn_extra_files(dir: str) -> None:
    print("Warning: git module '{}' has untracked files.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and add & commit your new files.", file=sys.stderr)


def chdir_prefix(dir: str) -> str:
    """Return the command to change to the target directory, plus '&&'."""
    if os.path.relpath(dir) != ".":
        return "cd " + pipes.quote(dir) + " && "
    else:
        return ""


def __tmp8(__tmp11, dir: str) -> None:
    print("Submodule '{}' not initialized.".format(__tmp11), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update --init {}".format(
        chdir_prefix(dir), __tmp11), file=sys.stderr)


def __tmp3(__tmp11: <FILL>, dir: str) -> None:
    print("Submodule '{}' not updated.".format(__tmp11), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update {}".format(
        chdir_prefix(dir), __tmp11), file=sys.stderr)
    print("(If you got this message because you updated {} yourself".format(__tmp11), file=sys.stderr)
    print(" then run \"git add {}\" to silence this check)".format(__tmp11), file=sys.stderr)


def __tmp5(__tmp7: str) -> None:
    """Verify the (submodule) integrity of a git repository.

    Potentially output warnings/errors (to stderr), and exit with status 1
    if we detected a severe problem.
    """
    __tmp7 = __tmp7 or '.'
    if not is_git_repo(__tmp7):
        return
    if not __tmp10():
        warn_no_git_executable()
        return
    for __tmp0 in __tmp2(__tmp7):
        submodule_path = os.path.join(__tmp7, __tmp0)
        if not is_git_repo(submodule_path):
            __tmp8(__tmp0, __tmp7)
            sys.exit(1)
        elif __tmp6(__tmp7, __tmp0) != __tmp9(submodule_path):
            __tmp3(__tmp0, __tmp7)
            sys.exit(1)
        elif __tmp1(submodule_path):
            warn_dirty(__tmp0)
        elif __tmp4(submodule_path):
            warn_extra_files(__tmp0)
