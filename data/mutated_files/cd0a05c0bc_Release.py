from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
#!/usr/bin/env python3

"""Add next release tag."""

from __future__ import annotations

import enum
import re
import subprocess

import click
import semver


class __typ1(enum.Enum):
    """Release target type."""

    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()


class Release:
    """Release."""

    __semver: semver.VersionInfo

    def __init__(__tmp1, version: __typ0):
        """Initialize Release.

        :param version: Version in format like "v1.2.3"
        """
        __tmp1.__semver = semver.parse_version_info(re.sub("^v", "", version))
        return

    def __str__(__tmp1) -> __typ0:
        """Return string.

        :returns: str
        """
        return "v" + __typ0(__tmp1.__semver)

    def __tmp3(__tmp1) -> __typ0:
        """Repr.

        :returns: repr
        """
        return f'Release(version="v{__typ0(__tmp1.__semver)}")'

    def next(__tmp1, __tmp0: __typ1) :
        """Return next release.

        :param target: Target to bump
        :returns: Next Release object
        :raises Exception: Unknown target type
        """
        next_semver: semver.VersionInfo
        if __tmp0 == __typ1.MAJOR:
            next_semver = __tmp1.__semver.bump_major()
        elif __tmp0 == __typ1.MINOR:
            next_semver = __tmp1.__semver.bump_minor()
        elif __tmp0 == __typ1.PATCH:
            next_semver = __tmp1.__semver.bump_patch()
        else:
            raise Exception(f"Unknown target {__tmp0}")
        return Release("v" + __typ0(next_semver))


def get_latest_release() -> Release:
    """Return latest release object.

    :returns: Latest Release object
    """
    # S603 subprocess call - check for execution of untrusted input.
    # S607 Starting a process with a partial executable path
    proc = subprocess.run(  # noqa: S603,S607
        ["git", "describe", "--tags", "--abbrev=0"], check=True, capture_output=True
    )
    tag = proc.stdout.decode("ascii").strip()
    return Release(tag)


def __tmp2(release: <FILL>) -> None:
    """Add release tag.

    Currently add tag to HEAD revision.

    :param release: Release object
    """
    cmd = ["git", "tag", "--sign", __typ0(release)]
    # S603 subprocess call - check for execution of untrusted input.
    subprocess.run(cmd, check=True)  # noqa: 603
    return


@click.command()
@click.option("--dryrun", is_flag=True)
@click.option("--major", "target", flag_value=__typ1.MAJOR)
@click.option("--minor", "target", flag_value=__typ1.MINOR)
@click.option("--patch", "target", flag_value=__typ1.PATCH, default=True)
def main(dryrun: __typ2, __tmp0) -> None:
    """tag_next_release entrypoint.

    :param dryrun: Dryrun flag
    :param target: Target to bump
    """
    latest = get_latest_release()
    next = latest.next(__tmp0)
    print(f"Latest release: {latest}")
    print(f"Next release:   {next}")
    if not dryrun:
        __tmp2(next)
    return


main()
