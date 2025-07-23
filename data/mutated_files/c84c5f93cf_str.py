from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""Utilities for verifying git integrity."""

# Used also from setup.py, so don't pull in anything additional here (like mypy or typing):
import os
import pipes
import subprocess
import sys

MYPY = False
if MYPY:
    from typing import Iterator


def __tmp3(dir: str) -> __typ0:
    """Is the given directory version-controlled with git?"""
    return os.path.exists(os.path.join(dir, ".git"))


def __tmp12() -> __typ0:
    """Can we run the git executable?"""
    try:
        subprocess.check_output(["git", "--help"])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False


def get_submodules(dir) -> "Iterator[str]":
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
        name = line.split(b" ")[1]
        yield name.decode(sys.getfilesystemencoding())


def __tmp9(dir: str) -> bytes:
    """Get the SHA-1 of the HEAD of a git repository."""
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dir).strip()


def __tmp8(dir: str, __tmp1: str) -> bytes:
    """Get the SHA-1 a submodule is supposed to have."""
    output = subprocess.check_output(["git", "ls-files", "-s", __tmp1], cwd=dir).strip()
    # E.g.: "160000 e4a7edb949e0b920b16f61aeeb19fc3d328f3012 0       typeshed"
    return output.split()[1]


def __tmp0(dir: str) :
    """Check whether a git repository has uncommitted changes."""
    output = subprocess.check_output(["git", "status", "-uno", "--porcelain"], cwd=dir)
    return output.strip() != b""


def __tmp4(dir: <FILL>) :
    """Check whether a git repository has untracked files."""
    output = subprocess.check_output(["git", "clean", "--dry-run", "-d"], cwd=dir)
    return output.strip() != b""


def warn_no_git_executable() -> None:
    print("Warning: Couldn't check git integrity. "
          "git executable not in path.", file=sys.stderr)


def __tmp11(dir: str) -> None:
    print("Warning: git module '{}' has uncommitted changes.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and commit or reset your changes", file=sys.stderr)


def __tmp5(dir: str) -> None:
    print("Warning: git module '{}' has untracked files.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and add & commit your new files.", file=sys.stderr)


def __tmp7(dir) -> str:
    """Return the command to change to the target directory, plus '&&'."""
    if os.path.relpath(dir) != ".":
        return "cd " + pipes.quote(dir) + " && "
    else:
        return ""


def error_submodule_not_initialized(name: str, dir: str) :
    print("Submodule '{}' not initialized.".format(name), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update --init {}".format(
        __tmp7(dir), name), file=sys.stderr)


def __tmp2(name: str, dir: str) -> None:
    print("Submodule '{}' not updated.".format(name), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update {}".format(
        __tmp7(dir), name), file=sys.stderr)
    print("(If you got this message because you updated {} yourself".format(name), file=sys.stderr)
    print(" then run \"git add {}\" to silence this check)".format(name), file=sys.stderr)


def __tmp6(__tmp10) -> None:
    """Verify the (submodule) integrity of a git repository.

    Potentially output warnings/errors (to stderr), and exit with status 1
    if we detected a severe problem.
    """
    __tmp10 = __tmp10 or '.'
    if not __tmp3(__tmp10):
        return
    if not __tmp12():
        warn_no_git_executable()
        return
    for __tmp1 in get_submodules(__tmp10):
        submodule_path = os.path.join(__tmp10, __tmp1)
        if not __tmp3(submodule_path):
            error_submodule_not_initialized(__tmp1, __tmp10)
            sys.exit(1)
        elif __tmp8(__tmp10, __tmp1) != __tmp9(submodule_path):
            __tmp2(__tmp1, __tmp10)
            sys.exit(1)
        elif __tmp0(submodule_path):
            __tmp11(__tmp1)
        elif __tmp4(submodule_path):
            __tmp5(__tmp1)
