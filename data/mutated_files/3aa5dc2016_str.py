# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# directories.py
# rosevomit.core.directories
# ___________________________________________________________________
"""This file contains the 'get_dir' function, which should theoretically be able to find any subdirectory of the Rosevomit directory from anywhere within the 'rosevomit' module or the associated repository. Theoretically."""
import glob
import os
import pathlib

from core import logs
from core.customerrors import RealityError

_DIRECTORIESLOGGER = logs.BaseLogger (__name__)


def __tmp2() :
    """Returns only the folder name of the current working directory, not the full path.

    Returns
    -------
    str
        The name of the current working directory.
    """
    _cwd = pathlib.Path.cwd()
    _path_split = os.path.split(_cwd)
    return _path_split[-1]


def __tmp1(__tmp0: <FILL>) -> pathlib.Path:
    """Returns the path of subdirectory of the 'rosevomit' directory. This function should work anywhere within the 'rosevomit' module or the associated repository.

    Parameters
    ----------
    ARG_dirname : str
        The name of the Rosevomit directory you're looking for.

    Returns
    -------
    _dirpath : pathlib.Path
        The path of the Rosevomit directory you're looking for.
    """
    # Let's assume we don't know where this function is being called from or to, and we don't know what the exact directory structure is that we're navigating through. Generally, all we know is that (1) our program Rosevomit is contained in a directory named 'rosevomit', and (2) the 'rosevomit' directory plus whatever directories we've created for documentation/testing/general development purposes should be contained in a directory called 'rosevomitrepo'. We also know (3) the name of the directory (ARG_dirname) we're looking for, which should be somewhere within the 'rosevomit' directory.
    #
    # We begin by finding out where we are.
    _cwd = pathlib.Path.cwd()
    # We need a known starting place to begin navigating. This can be either our 'rosevomit' directory or our 'rosevomitrepo' directory.
    _path_parts = pathlib.PurePath (_cwd).parts
    if "rosevomit" in _path_parts:
        _path_partslist = list(_path_parts)
        while _path_partslist[-1] != "rosevomit":
            _path_partslist.pop()
        _path = os.path.join (*_path_partslist)  # The '*' is a "splat" operator
        rosevomit_directory = pathlib.PurePath (_path)
        os.chdir ("..")
        repository_directory = pathlib.PurePath (pathlib.Path.cwd())
    # If the 'rosevomit' directory isn't in _path_parts, then that's a problem. We'll attempt to work around it by looking for the 'rosevomitrepo' directory. At the end of the day, we need *some* sort of place to begin navigating around the filesystem.
    elif "rosevomitrepo" in _path_parts:
        _path_partslist = list(_path_parts)
        while _path_partslist[-1] != "rosevomitrepo":
            _path_partslist.pop()
        _path = os.path.join (*_path_partslist)  # The '*' is a "splat" operator
        repository_directory = pathlib.PurePath (_path)
    else:
        # If neither 'rosevomit' nor 'rosevomitrepo' show up in our path, we're well and truly lost. Let's raise an exception (a Python error).
        raise FileNotFoundError

    # TODO: Honestly, we should split the part of the function above this comment into it's own function. Otherwise, we're exceeding a single responsibility for this function.

    # Now that we've established which parts of the expected Rosevomit filesystem we can find, we navigate to the best available location to look for the subdirectory.
    # TODO: There's a *lot* of advice online about how checking for variable existence in Python is not a good way to handle flow control... so this next part probably needs refactoring.
    if "rosevomit_directory" in locals():  # exists
        os.chdir (rosevomit_directory)
        os.chdir (f"{__tmp0}")
    elif "repository_directory" in locals():  # exists
        os.chdir (repository_directory)
        possible_paths = glob.glob (f"*/{__tmp0}", recursive=True)
        num_possible_paths = len (possible_paths)
        if num_possible_paths == 1:
            os.chdir (possible_paths[0])
        elif num_possible_paths == 0:
            raise FileNotFoundError
        else:
            # If multiple paths are returned, something has gone wrong and we need to stop.
            raise ValueError
    else:
        raise RealityError("This should definitely 100% never happen.")
    _dirpath = pathlib.Path.cwd()
    # Finally, return to where we started
    os.chdir (_cwd)
    return _dirpath
