# This Python file uses the following encoding: utf-8
"""The 'messages.py' file contains messages that are displayed in multiple places throughout the testing module. They do not accept user input - they merely display a message."""

import sys
import textwrap
import traceback

def __tmp0():
    """Prints a traceback message"""
    print ("ERROR MESSAGE: AN ERROR OCCURED.")
    print ()
    print ("ERROR MESSAGE: Short traceback, a.k.a. print_exc(1):")
    traceback.print_exc (limit=1, file=sys.stdout)
    print ()
    print ("ERROR MESSAGE: Full traceback, a.k.a. print_exc():")
    traceback.print_exc (file=sys.stdout)


def __tmp2 (__tmp3):
    """Prints a message regarding a test that successfully finished."""
    print (textwrap.fill (f"The {__tmp3} test finished successfully. Please see the test's output file for the results."))


def __tmp1 (__tmp3:<FILL>): # TODO: Include an exception name or traceback
    """Prints a message regarding a test that failed to successfully finish."""
    print (textwrap.fill (f"The {__tmp3} test did NOT finish successfully. Please see the test's output file for the results."))
