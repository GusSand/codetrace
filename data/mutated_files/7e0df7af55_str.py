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


def is_git_repo(dir) :
    """Is the given directory version-controlled with git?"""
    return os.path.exists(os.path.join(dir, ".git"))


def have_git() :
    """Can we run the git executable?"""
    try:
        subprocess.check_output(["git", "--help"])
        return True
    except subprocess.CalledProcessError:
        return False
    except OSError:
        return False


def get_submodules(dir: str) :
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
        __tmp4 = line.split(b" ")[1]
        yield __tmp4.decode(sys.getfilesystemencoding())


def git_revision(dir) -> __typ0:
    """Get the SHA-1 of the HEAD of a git repository."""
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=dir).strip()


def submodule_revision(dir, submodule) :
    """Get the SHA-1 a submodule is supposed to have."""
    output = subprocess.check_output(["git", "ls-files", "-s", submodule], cwd=dir).strip()
    # E.g.: "160000 e4a7edb949e0b920b16f61aeeb19fc3d328f3012 0       typeshed"
    return output.split()[1]


def is_dirty(dir) :
    """Check whether a git repository has uncommitted changes."""
    output = subprocess.check_output(["git", "status", "-uno", "--porcelain"], cwd=dir)
    return output.strip() != b""


def __tmp0(dir) :
    """Check whether a git repository has untracked files."""
    output = subprocess.check_output(["git", "clean", "--dry-run", "-d"], cwd=dir)
    return output.strip() != b""


def __tmp2() :
    print("Warning: Couldn't check git integrity. "
          "git executable not in path.", file=sys.stderr)


def warn_dirty(dir: str) :
    print("Warning: git module '{}' has uncommitted changes.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and commit or reset your changes", file=sys.stderr)


def warn_extra_files(dir) -> None:
    print("Warning: git module '{}' has untracked files.".format(dir),
          file=sys.stderr)
    print("Go to the directory", file=sys.stderr)
    print("  {}".format(dir), file=sys.stderr)
    print("and add & commit your new files.", file=sys.stderr)


def __tmp1(dir) :
    """Return the command to change to the target directory, plus '&&'."""
    if os.path.relpath(dir) != ".":
        return "cd " + pipes.quote(dir) + " && "
    else:
        return ""


def error_submodule_not_initialized(__tmp4, dir) :
    print("Submodule '{}' not initialized.".format(__tmp4), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update --init {}".format(
        __tmp1(dir), __tmp4), file=sys.stderr)


def error_submodule_not_updated(__tmp4, dir: <FILL>) :
    print("Submodule '{}' not updated.".format(__tmp4), file=sys.stderr)
    print("Please run:", file=sys.stderr)
    print("  {}git submodule update {}".format(
        __tmp1(dir), __tmp4), file=sys.stderr)
    print("(If you got this message because you updated {} yourself".format(__tmp4), file=sys.stderr)
    print(" then run \"git add {}\" to silence this check)".format(__tmp4), file=sys.stderr)


def verify_git_integrity_or_abort(__tmp3: str) :
    """Verify the (submodule) integrity of a git repository.

    Potentially output warnings/errors (to stderr), and exit with status 1
    if we detected a severe problem.
    """
    __tmp3 = __tmp3 or '.'
    if not is_git_repo(__tmp3):
        return
    if not have_git():
        __tmp2()
        return
    for submodule in get_submodules(__tmp3):
        submodule_path = os.path.join(__tmp3, submodule)
        if not is_git_repo(submodule_path):
            error_submodule_not_initialized(submodule, __tmp3)
            sys.exit(1)
        elif submodule_revision(__tmp3, submodule) != git_revision(submodule_path):
            error_submodule_not_updated(submodule, __tmp3)
            sys.exit(1)
        elif is_dirty(submodule_path):
            warn_dirty(submodule)
        elif __tmp0(submodule_path):
            warn_extra_files(submodule)
