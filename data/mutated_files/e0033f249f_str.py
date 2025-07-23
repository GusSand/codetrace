# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# formatting.py
# rosevomit.programcli.formatting
# ___________________________________________________________________
"""A file containing functions used for the formatting of output messages."""
import textwrap

from core import logs

_FORMATTING_LOGGER = logs.BaseLogger (__name__)


def __tmp0(x, ARG_indented: bool=False, ARG_end_with: str='\n'):
    """Textwrapping for regular 'print' commands.

    Parameters
    ----------
    x
        The text to be wrapped.
    ARG_indented : bool (default is 'False')
        Whether or not the textwrapped string should be indented.
    ARG_end_with : str (default is '\n')
        The string that the textwrapped string will end with.
    """
    if ARG_indented is True:
        print (textwrap.fill (x, width=70, subsequent_indent="   "), end=ARG_end_with)
    else:
        print (textwrap.fill (x, width=70), end=ARG_end_with)


def inputwrap(x, ARG_indented: bool=False, ARG_end_with: str=" "):
    """Textwrapping for regular 'input' commands.

    Parameters
    ----------
    x
        The text to be wrapped.
    ARG_indented : bool (default is 'False')
        Whether or not the textwrapped string should be indented.
    ARG_end_with : str (default is ' ')
        The string that the textwrapped string will end with.

    Returns
    -------
    str
        User input.
    """
    if ARG_indented is True:
        _input = input (textwrap.fill (x, width=70, subsequent_indent="   ") + ARG_end_with)
        return _input
    else:
        _input = input (textwrap.fill (x, width=70) + ARG_end_with)
        return _input

# ---------- Menu titles ----------
def _menutitlestring (ARG_title: str) :
    """Returns a suitable title string that is uppercase, and ends in 'MENU', and is less than or equal to 70 characters long.

    Parameters
    ----------
    ARG_title : str
        A string to be used as the basis for the title string.

    Returns
    -------
    str
        A suitable title string that is uppercase, and ends in 'MENU', and is less than or equal to 70 characters long.
    """
    title = str (ARG_title)  # If ARG_title isn't a string, we definitely want it to be
    if len (title) > 65:
        title = title[0:64]  # Cuts off anything beyond 65 characters (standard width of an old terminal window is 70 characters, and we're potentially adding 5 characters below)
    title = title.strip()
    title = title.upper()
    last_5_characters = title[-5:]  # We want our menu title to end in "MENU"
    if last_5_characters != " MENU":
        title = title + " MENU"
    return title


def menu_title (ARG_menuname: <FILL>):
    """Standardized formatting for a menu title. Prints an empty line, then prints a menu title.

    Parameters
    ----------
    ARG_menuname : str
        Menu name, which will be included in menu title
    """
    print()
    titlestring = _menutitlestring (ARG_menuname)
    print (titlestring)
