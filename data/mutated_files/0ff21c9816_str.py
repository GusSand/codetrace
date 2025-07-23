# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# _dynamic_constants.py
# rosevomit.core._dynamic_constants
# ___________________________________________________________________
"""This file contains the functions that generate the dynamic constants."""
from distutils.util import strtobool
import os
import pathlib
from xml.etree import ElementTree

from core import directories, logs
# from core.utilities import debugmessage

_DYNAMICCONSTANTSLOGGER = logs.BaseLogger (__name__)


def __tmp2 (__tmp1: <FILL>) :
    """Returns the path to a Rosevomit subdirectory. Basically a wrapper for core.directories.get_dir().

    If the path cannot be found, this function will *not* surpress any exceptions.

    Parameters
    ----------
    ARG_dirname : str
        The name of the Rosevomit directory you're looking for.

    Returns
    -------
    pathlib.Path
        A path returned from core.directories.get_dir().
    """
    _result = directories.get_dir (__tmp1)
    return _result


def __tmp0 (__tmp1: str) :
    """Returns the path to a Rosevomit subdirectory. Basically a wrapper for core.directories.get_dir().

    If FileNotFoundErrors or ValueErrors arise, this function will surpress those errors and return "None".

    Parameters
    ----------
    ARG_dirname : str
        The name of the Rosevomit directory you're looking for.

    Returns
    -------
    pathlib.Path or NoneType
        A path returned from core.directories.get_dir(), or None if FileNotFoundError or ValueError are raised.
    """
    try:
        _result = directories.get_dir (__tmp1)
    except (FileNotFoundError, ValueError) as e:
        # debugmessage (e)
        _result = None
    return _result


def get_version_number(__tmp3):
    """Gets the version number.

    Parameters
    ----------
    ARG_core_directory : pathlib.Path
        The path to Rosevomit's core directory.

    Returns
    -------
    major_version : str or NoneType
        The program's major version number.
    minor_version : str or NoneType
        The program's minor version number.
    patch_version : str ot NoneType
        The program's patch version number.
    is_devbuild : bool
        True if this program is a dev version, else False.
    """
    try:
        # debugmessage ("Getting version number...", end=" ")
        os.chdir (__tmp3)
        _tree = ElementTree.parse ("Version.xml")
        _root = _tree.getroot ()
        _human_version = _root.findall("./version[@type='human']//")
        for child in _human_version:
            if child.tag == "major":
                major_version = child.text
            elif child.tag == "minor":
                minor_version = child.text
            elif child.tag == "patch":
                patch_version = child.text
            else:
                raise IOError
        _devbuild = _root.findtext("devbuild", default="False")
        _devbuild = strtobool (_devbuild)  # Because the 'findtext' function above returns a string, not a bool. pylint: disable=invalid-name
        is_devbuild = bool (_devbuild)  # And because, despite its name, 'strtobool()' returns an integer (1 or 0), not a bool
        # debugmessage ("done.")
    except FileNotFoundError:
        # debugmessage ("error.")
        print ("ERROR: COULD NOT FIND VERSION FILE.")
    except IOError:
        # debugmessage ("error.")
        print ("ERROR: VERSION FILE IS INCOMPLETE OR FORMATTED INCORRECTLY.")
    else:
        return major_version, minor_version, patch_version, is_devbuild
