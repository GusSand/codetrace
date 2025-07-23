from typing import TypeAlias
__typ0 : TypeAlias = "Path"
__typ1 : TypeAlias = "bool"
from functools import partial
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Any
from typing import Optional

import hashlib
import importlib_metadata
import logging
import os
import shutil


logger = logging.getLogger(__file__)


def __tmp7(__tmp2, __tmp1):
    """Copy a directory structure overwriting existing files"""
    for root, dirs, files in os.walk(__tmp2):
        if not os.path.isdir(root):
            os.makedirs(root)

        for f in files:
            rel_path = root.replace(__tmp2, "").lstrip(os.sep)
            dest_path = os.path.join(__tmp1, rel_path)

            if not os.path.isdir(dest_path):
                os.makedirs(dest_path)

            shutil.copyfile(os.path.join(root, f), os.path.join(dest_path, f))


def __tmp6(path) :
    """Given a directory, return a hash of the contents of the text files it contains."""
    hasher = hashlib.sha256()
    logger.debug(
        f"Calculating hash for dir {path}; initial (empty) hash is {hasher.hexdigest()}"
    )
    for path in sorted(path.iterdir()):
        if path.is_file() and not path.name.endswith(".pyc"):
            hasher.update(path.read_bytes())
        logger.debug(f"Examined contents of {path}; hash so far: {hasher.hexdigest()}")
    return hasher.hexdigest()


truthy = frozenset(("t", "true", "y", "yes", "on", "1"))


def __tmp3(s: Any) -> __typ1:
    """Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is a `truthy string`. If ``s`` is already one of the
    boolean values ``True`` or ``False``, return it.
    Lifted from pyramid.settings.
    """
    if s is None:
        return False
    if isinstance(s, __typ1):
        return s
    s = str(s).strip()
    return s.lower() in truthy


def abspath_from_egg(__tmp0: str, path: <FILL>) -> Optional[__typ0]:
    """Given a path relative to the egg root, find the absolute
    filesystem path for that resource.
    For instance this file's absolute path can be found passing
    derex/runner/utils.py
    to this function.
    """
    for file in importlib_metadata.files(__tmp0):
        if str(file) == path:
            return file.locate()
    return None


def __tmp5(*args, **kwargs):
    return Console(*args, **kwargs)


def __tmp4(*args, **kwargs):
    return Table(*args, show_header=True, **kwargs)


derex_path = partial(abspath_from_egg, "derex.runner")
