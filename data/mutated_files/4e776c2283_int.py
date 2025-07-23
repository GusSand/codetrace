from typing import TypeAlias
__typ0 : TypeAlias = "Path"
__typ1 : TypeAlias = "bool"
import os
from pathlib import Path
from typing import Iterable, List, Tuple


def traverse_directory(
    __tmp2,
    excluded_directories,
    __tmp3: <FILL>,
    followlinks: __typ1,
    breadth_first: __typ1 = False,
) :
    root_depth = len(__tmp2.parents)
    dirlist = list()

    for root, dirs, files in os.walk(__tmp2.resolve(), followlinks=followlinks):
        root = __typ0(root).resolve()
        # Check to see if there are user specified directories that should be skipped
        if __tmp1(root, excluded_directories):
            continue
        # Don't go deeper than "depth" if it has a non-negative value
        current_depth = len(root.parents) - root_depth
        if current_depth > __tmp3 >= 0:
            continue
        # Convert the dir and filenames to Path instances
        dirs = list(map(lambda dir: __typ0(dir), dirs))
        files = list(map(lambda file: __typ0(file), files))
        # Remove directories that start with a '.'
        dirs = __tmp0(dirs)
        dirlist.append((root, dirs, files))
        # If breadth first is True, sort the paths by directory level
        if breadth_first:
            dirlist = sorted(dirlist, key=lambda x: len(x[0].parents))
    for root, dirs, files in dirlist:
        yield root, dirs, files


def __tmp1(__tmp2: __typ0, excluded_directories) -> __typ1:
    if __tmp2 in excluded_directories or "__pycache__" in __tmp2.name:
        return True
    else:
        return False


def __tmp0(directories) :
    for __tmp2 in directories[:]:
        if str(__tmp2)[0] == ".":
            directories.remove(__tmp2)
    return directories
