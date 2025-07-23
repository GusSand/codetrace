# This Python file uses the following encoding: utf-8
"""Contains miscellaneous functions."""
import os
import pathlib
import sys
import traceback


def __tmp0 (basename: <FILL>) :
    """If the basename isn't unique within the current working directory, this function adds an integer to the end of the basename and increments it until it becomes unique."""
    number = 1
    name = basename
    while os.path.exists (name) is True:
        number = number + 1
        name = basename + "-" + str(number)
    return name


def __tmp4():
    """Returns only the folder name of the current working directory, not the full path."""
    _cwd = pathlib.Path.cwd()
    _path_split = os.path.split(_cwd)
    return _path_split[-1]

# THANKS: https://stackoverflow.com/questions/2828953/silence-the-stdout-of-a-function-in-python-without-trashing-sys-stdout-and-resto/40054132#40054132
class __typ0(object):
    """Silences stdout of a function without wrapping a function all.

    Usage:
    with Suppressor():
        DoMyFunction(*args,**kwargs)
    """
    def __tmp2(__tmp1):
        __tmp1.stdout = sys.stdout
        sys.stdout = __tmp1

    def __tmp3(__tmp1, type, value, traceback):
        sys.stdout = __tmp1.stdout
        if type is not None:
            # Do normal exception handling
            raise

    def write(__tmp1, __tmp5):
        pass
