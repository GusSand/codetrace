from typing import TypeAlias
__typ0 : TypeAlias = "str"
#!/usr/bin/env python3

"""Add next release tag."""

from __future__ import annotations

import enum
import re
import subprocess

import click
import semver


class __typ2(enum.Enum):
    """Release target type."""

    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()


class __typ1:
    """Release."""

    __semver: semver.VersionInfo

    def __tmp5(__tmp2, __tmp0: __typ0):
        """Initialize Release.

        :param version: Version in format like "v1.2.3"
        """
        __tmp2.__semver = semver.parse_version_info(re.sub("^v", "", __tmp0))
        return

    def __tmp6(__tmp2) :
        """Return string.

        :returns: str
        """
        return "v" + __typ0(__tmp2.__semver)

    def __repr__(__tmp2) :
        """Repr.

        :returns: repr
        """
        return f'Release(version="v{__typ0(__tmp2.__semver)}")'

    def next(__tmp2, target: __typ2) :
        """Return next release.

        :param target: Target to bump
        :returns: Next Release object
        :raises Exception: Unknown target type
        """
        next_semver: semver.VersionInfo
        if target == __typ2.MAJOR:
            next_semver = __tmp2.__semver.bump_major()
        elif target == __typ2.MINOR:
            next_semver = __tmp2.__semver.bump_minor()
        elif target == __typ2.PATCH:
            next_semver = __tmp2.__semver.bump_patch()
        else:
            raise Exception(f"Unknown target {target}")
        return __typ1("v" + __typ0(next_semver))


def __tmp3() :
    """Return latest release object.

    :returns: Latest Release object
    """
    # S603 subprocess call - check for execution of untrusted input.
    # S607 Starting a process with a partial executable path
    proc = subprocess.run(  # noqa: S603,S607
        ["git", "describe", "--tags", "--abbrev=0"], check=True, capture_output=True
    )
    tag = proc.stdout.decode("ascii").strip()
    return __typ1(tag)


def __tmp7(__tmp4: __typ1) :
    """Add release tag.

    Currently add tag to HEAD revision.

    :param release: Release object
    """
    cmd = ["git", "tag", "--sign", __typ0(__tmp4)]
    # S603 subprocess call - check for execution of untrusted input.
    subprocess.run(cmd, check=True)  # noqa: 603
    return


@click.command()
@click.option("--dryrun", is_flag=True)
@click.option("--major", "target", flag_value=__typ2.MAJOR)
@click.option("--minor", "target", flag_value=__typ2.MINOR)
@click.option("--patch", "target", flag_value=__typ2.PATCH, default=True)
def __tmp1(dryrun: <FILL>, target) -> None:
    """tag_next_release entrypoint.

    :param dryrun: Dryrun flag
    :param target: Target to bump
    """
    latest = __tmp3()
    next = latest.next(target)
    print(f"Latest release: {latest}")
    print(f"Next release:   {next}")
    if not dryrun:
        __tmp7(next)
    return


__tmp1()
