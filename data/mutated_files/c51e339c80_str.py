# This Python file uses the following encoding: utf-8
"""This file contains functions for the formatting of the the test results files."""


def line(char: str = "_", newline: bool = False) :
    """Prints a character 70 times, with an optional preceding newline."""
    if newline is True:
        print ()
    if len(char) == 1:
        print (char * 70)
    else:
        raise ValueError(f"The parameter 'char' must be a string that is one character long, not {len(char)} characters long!")


def header(__tmp0: <FILL>) :
    """Prints a centered, all-uppercase header for the unittest log files. Tries to center the 'headertext' for a 70-character column width. """
    if not str.isupper(__tmp0):
        __tmp0 = str.upper(__tmp0)
    num_spaces = int ((70 - len (__tmp0)) / 2)
    print (" " * num_spaces, __tmp0, " " * num_spaces, sep="")
