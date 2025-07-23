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


def __tmp6(dir) :
    """Is the given directory version-controlled with git?"""
    return os.path.exists(os.path.join(dir, ".git"))


def __tmp1() :
    """Can we run the git executable?"""
    try:
        subprocess.check_output(["git", "--help"])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False


def __tmp3(dir) :
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
        __tmp16 = line.split(b" ")[1]
        yield __tmp16.decode(sys.getfilesystemencoding())


def __tmp14(dir) :
    """Get the SHA-1 of the HEAD of a git repository."""
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dir).strip()


def __tmp9(dir, __tmp2) :
    """Get the SHA-1 a submodule is supposed to have."""
    output = subprocess.check_output(["git", "ls-files", "-s", __tmp2], cwd=dir).strip()
    # E.g.: "160000 e4a7edb949e0b920b16f61aeeb19fc3d328f3012 0       typeshed"
    return output.split()[1]


def __tmp4(dir: <FILL>) -> __typ1:
    """Check whether a git repository has uncommitted changes."""
    output = subprocess.check_output(["git", "status", "-uno", "--porcelain"], cwd=dir)
    return output.strip() != b""


def __tmp7(dir) -> __typ1:
    """Check whether a git repository has untracked files."""
    output = subprocess.check_output(["git", "clean", "--dry-run", "-d"], cwd=dir)
    return output.strip() != b""


def __tmp0() :
    print("Warning: Couldn't check git integrity. "
          "git executable not in path.", file=sys.stderr)


def __tmp11(dir) :
    print("Warning: git module '{}' has uncommitted changes.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and commit or reset your changes", file=sys.stderr)


def __tmp15(dir) :
    print("Warning: git module '{}' has untracked files.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and add & commit your new files.", file=sys.stderr)


def __tmp10(dir) :
    """Return the command to change to the target directory, plus '&&'."""
    if os.path.relpath(dir) != ".":
        return "cd " + pipes.quote(dir) + " && "
    else:
        return ""


def __tmp13(__tmp16: str, dir) :
    print("Submodule '{}' not initialized.".format(__tmp16), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update --init {}".format(
        __tmp10(dir), __tmp16), file=sys.stderr)


def __tmp5(__tmp16, dir: str) :
    print("Submodule '{}' not updated.".format(__tmp16), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update {}".format(
        __tmp10(dir), __tmp16), file=sys.stderr)
    print("(If you got this message because you updated {} yourself".format(__tmp16), file=sys.stderr)
    print(" then run \"git add {}\" to silence this check)".format(__tmp16), file=sys.stderr)


def __tmp8(__tmp12) :
    """Verify the (submodule) integrity of a git repository.

    Potentially output warnings/errors (to stderr), and exit with status 1
    if we detected a severe problem.
    """
    __tmp12 = __tmp12 or '.'
    if not __tmp6(__tmp12):
        return
    if not __tmp1():
        __tmp0()
        return
    for __tmp2 in __tmp3(__tmp12):
        submodule_path = os.path.join(__tmp12, __tmp2)
        if not __tmp6(submodule_path):
            __tmp13(__tmp2, __tmp12)
            sys.exit(1)
        elif __tmp9(__tmp12, __tmp2) != __tmp14(submodule_path):
            __tmp5(__tmp2, __tmp12)
            sys.exit(1)
        elif __tmp4(submodule_path):
            __tmp11(__tmp2)
        elif __tmp7(submodule_path):
            __tmp15(__tmp2)
