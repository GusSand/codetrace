import os
from pathlib import Path
from typing import Iterable, List, Tuple


def __tmp6(
    __tmp1: <FILL>,
    __tmp4,
    __tmp7,
    __tmp5,
    breadth_first: bool = False,
) :
    root_depth = len(__tmp1.parents)
    dirlist = list()

    for root, dirs, files in os.walk(__tmp1.resolve(), __tmp5=__tmp5):
        root = Path(root).resolve()
        # Check to see if there are user specified directories that should be skipped
        if __tmp0(root, __tmp4):
            continue
        # Don't go deeper than "depth" if it has a non-negative value
        current_depth = len(root.parents) - root_depth
        if current_depth > __tmp7 >= 0:
            continue
        # Convert the dir and filenames to Path instances
        dirs = list(map(lambda dir: Path(dir), dirs))
        files = list(map(lambda file: Path(file), files))
        # Remove directories that start with a '.'
        dirs = __tmp2(dirs)
        dirlist.append((root, dirs, files))
        # If breadth first is True, sort the paths by directory level
        if breadth_first:
            dirlist = sorted(dirlist, key=lambda x: len(x[0].parents))
    for root, dirs, files in dirlist:
        yield root, dirs, files


def __tmp0(__tmp1, __tmp4) :
    if __tmp1 in __tmp4 or "__pycache__" in __tmp1.name:
        return True
    else:
        return False


def __tmp2(__tmp3) -> List[Path]:
    for __tmp1 in __tmp3[:]:
        if str(__tmp1)[0] == ".":
            __tmp3.remove(__tmp1)
    return __tmp3
