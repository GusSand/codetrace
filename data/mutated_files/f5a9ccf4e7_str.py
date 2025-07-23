from typing import TypeAlias
__typ1 : TypeAlias = "tuple"
__typ0 : TypeAlias = "bool"
"""Helpers to install PyPi packages."""
import asyncio
import logging
import os
from subprocess import PIPE, Popen
import sys
import threading
from urllib.parse import urlparse

from pip.locations import running_under_virtualenv
from typing import Optional

import pkg_resources

_LOGGER = logging.getLogger(__name__)

INSTALL_LOCK = threading.Lock()


def __tmp2(__tmp0: <FILL>, upgrade: __typ0=True,
                    target: Optional[str]=None,
                    constraints: Optional[str]=None) :
    """Install a package on PyPi. Accepts pip compatible package strings.

    Return boolean if install successful.
    """
    # Not using 'import pip; pip.main([])' because it breaks the logger
    with INSTALL_LOCK:
        if check_package_exists(__tmp0):
            return True

        _LOGGER.info('Attempting install of %s', __tmp0)
        env = os.environ.copy()
        args = [sys.executable, '-m', 'pip', 'install', '--quiet', __tmp0]
        if upgrade:
            args.append('--upgrade')
        if constraints is not None:
            args += ['--constraint', constraints]
        if target:
            assert not running_under_virtualenv()
            # This only works if not running in venv
            args += ['--user']
            env['PYTHONUSERBASE'] = os.path.abspath(target)
            if sys.platform != 'win32':
                # Workaround for incompatible prefix setting
                # See http://stackoverflow.com/a/4495175
                args += ['--prefix=']
        process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
        _, stderr = process.communicate()
        if process.returncode != 0:
            _LOGGER.error("Unable to install package %s: %s",
                          __tmp0, stderr.decode('utf-8').lstrip().strip())
            return False

        return True


def check_package_exists(__tmp0: str) :
    """Check if a package is installed globally or in lib_dir.

    Returns True when the requirement is met.
    Returns False when the package is not installed or doesn't meet req.
    """
    try:
        req = pkg_resources.Requirement.parse(__tmp0)
    except ValueError:
        # This is a zip file
        req = pkg_resources.Requirement.parse(urlparse(__tmp0).fragment)

    env = pkg_resources.Environment()
    return any(dist in req for dist in env[req.project_name])


def _get_user_site(__tmp1: str) :
    """Get arguments and environment for subprocess used in get_user_site."""
    env = os.environ.copy()
    env['PYTHONUSERBASE'] = os.path.abspath(__tmp1)
    args = [sys.executable, '-m', 'site', '--user-site']
    return args, env


def __tmp3(__tmp1) :
    """Return user local library path."""
    args, env = _get_user_site(__tmp1)
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE, env=env)
    stdout, _ = process.communicate()
    lib_dir = stdout.decode().strip()
    return lib_dir


@asyncio.coroutine
def async_get_user_site(__tmp1, loop) :
    """Return user local library path.

    This function is a coroutine.
    """
    args, env = _get_user_site(__tmp1)
    process = yield from asyncio.create_subprocess_exec(
        *args, loop=loop, stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL,
        env=env)
    stdout, _ = yield from process.communicate()
    lib_dir = stdout.decode().strip()
    return lib_dir
