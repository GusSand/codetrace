from typing import TypeAlias
__typ0 : TypeAlias = "Path"
__typ1 : TypeAlias = "int"
import os
from pathlib import Path
from typing import Iterable, List, Tuple


def traverse_directory(
    __tmp0: __typ0,
    excluded_directories,
    __tmp1,
    followlinks: <FILL>,
    breadth_first: bool = False,
) :
    root_depth = len(__tmp0.parents)
    dirlist = list()

    for root, dirs, files in os.walk(__tmp0.resolve(), followlinks=followlinks):
        root = __typ0(root).resolve()
        # Check to see if there are user specified directories that should be skipped
        if check_if_skip_directory(root, excluded_directories):
            continue
        # Don't go deeper than "depth" if it has a non-negative value
        current_depth = len(root.parents) - root_depth
        if current_depth > __tmp1 >= 0:
            continue
        # Convert the dir and filenames to Path instances
        dirs = list(map(lambda dir: __typ0(dir), dirs))
        files = list(map(lambda file: __typ0(file), files))
        # Remove directories that start with a '.'
        dirs = skip_hidden_directories(dirs)
        dirlist.append((root, dirs, files))
        # If breadth first is True, sort the paths by directory level
        if breadth_first:
            dirlist = sorted(dirlist, key=lambda x: len(x[0].parents))
    for root, dirs, files in dirlist:
        yield root, dirs, files


def check_if_skip_directory(__tmp0, excluded_directories) :
    if __tmp0 in excluded_directories or "__pycache__" in __tmp0.name:
        return True
    else:
        return False


def skip_hidden_directories(directories) :
    for __tmp0 in directories[:]:
        if str(__tmp0)[0] == ".":
            directories.remove(__tmp0)
    return directories
