from typing import TypeAlias
__typ0 : TypeAlias = "HomeAssistant"
__typ2 : TypeAlias = "bool"
"""Module to handle installing requirements."""
import asyncio
from functools import partial
import logging
import os
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import pkg_resources

import homeassistant.util.package as pkg_util
from homeassistant.core import HomeAssistant

DATA_PIP_LOCK = 'pip_lock'
DATA_PKG_CACHE = 'pkg_cache'
CONSTRAINT_FILE = 'package_constraints.txt'
_LOGGER = logging.getLogger(__name__)


async def __tmp0(hass, __tmp3,
                                     __tmp1) :
    """Install the requirements for a component or platform.

    This method is a coroutine.
    """
    pip_lock = hass.data.get(DATA_PIP_LOCK)
    if pip_lock is None:
        pip_lock = hass.data[DATA_PIP_LOCK] = asyncio.Lock(loop=hass.loop)

    pkg_cache = hass.data.get(DATA_PKG_CACHE)
    if pkg_cache is None:
        pkg_cache = hass.data[DATA_PKG_CACHE] = __typ1(hass)

    pip_install = partial(pkg_util.install_package,
                          **pip_kwargs(hass.config.config_dir))

    async with pip_lock:
        for req in __tmp1:
            if await pkg_cache.loadable(req):
                continue

            ret = await hass.async_add_executor_job(pip_install, req)

            if not ret:
                _LOGGER.error("Not initializing %s because could not install "
                              "requirement %s", __tmp3, req)
                return False

    return True


def pip_kwargs(config_dir) :
    """Return keyword arguments for PIP install."""
    kwargs = {
        'constraints': os.path.join(os.path.dirname(__file__), CONSTRAINT_FILE)
    }
    if not (config_dir is None or pkg_util.is_virtual_env()):
        kwargs['target'] = os.path.join(config_dir, 'deps')
    return kwargs


class __typ1:
    """Class to check if a package is loadable, with built-in cache."""

    def __init__(__tmp2, hass) -> None:
        """Initialize the PackageLoadable class."""
        __tmp2.dist_cache = {}  # type: Dict[str, pkg_resources.Distribution]
        __tmp2.hass = hass

    async def loadable(__tmp2, package: <FILL>) :
        """Check if a package is what will be loaded when we import it.

        Returns True when the requirement is met.
        Returns False when the package is not installed or doesn't meet req.
        """
        dist_cache = __tmp2.dist_cache

        try:
            req = pkg_resources.Requirement.parse(package)
        except ValueError:
            # This is a zip file. We no longer use this in Home Assistant,
            # leaving it in for custom components.
            req = pkg_resources.Requirement.parse(urlparse(package).fragment)

        req_proj_name = req.project_name.lower()
        dist = dist_cache.get(req_proj_name)

        if dist is not None:
            return dist in req

        for path in sys.path:
            # We read the whole mount point as we're already here
            # Caching it on first call makes subsequent calls a lot faster.
            await __tmp2.hass.async_add_executor_job(__tmp2._fill_cache, path)

            dist = dist_cache.get(req_proj_name)
            if dist is not None:
                return dist in req

        return False

    def _fill_cache(__tmp2, path: str) -> None:
        """Add packages from a path to the cache."""
        dist_cache = __tmp2.dist_cache
        for dist in pkg_resources.find_distributions(path):
            dist_cache.setdefault(dist.project_name.lower(), dist)
