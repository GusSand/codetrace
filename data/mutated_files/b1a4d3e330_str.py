from typing import TypeAlias
__typ0 : TypeAlias = "dict"
# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# worsecli.py
# rosevomit.programcli.worsecli
# ___________________________________________________________________
"""A file containing the base functions for a command line interface dialog."""
from distutils.util import strtobool
import re
from typing import Union

from core import logs, REGEXES_NO, REGEXES_YES
from programcli import formatting, messages

_DIALOG_LOGGER = logs.BaseLogger (__name__)

# ---------- Prompts ----------
def __tmp0 (ARG_default: bool) :
    """Determines which prompt hint to show the user.

    Parameters
    ----------
    ARG_default : bool
        Determines which prompt hint to return.

    Returns
    -------
    str
        The prompt hint. If 'True', returns '([Yes]/No)'. If 'False', returns '(Yes/[No])'.
    """
    if ARG_default is True:
        return "([Yes]/No)"
    elif ARG_default is False:
        return "(Yes/[No])"
    else:
        raise TypeError ("ARG_default must be bool.")


def prompt_generic (ARG_prompt) :
    """Displays a prompt, accepts input, cleans it, and returns it.

    Parameters
    ----------
    ARG_prompt : str
        Prompt to display.

    Returns
    -------
    str
        User's input in response to the prompt.
    """
    _input = formatting.inputwrap (ARG_prompt)
    result = _input.strip()
    if result == "":
        messages.unrecognized_input_message (result)
        recursive_result = prompt_generic (ARG_prompt)
        result = recursive_result
    return result


def prompt_yesno (ARG_prompt: <FILL>, ARG_default: bool=True) -> bool:
    """Asks the user a yes/no question, and returns the result as a bool.

    Parameters
    ----------
    ARG_prompt : str
        Prompt to display.
    ARG_default : bool, defaults to True
        The boolean value to return if the user inputs nothing. Also determines which prompt hint will be displayed to the user.

    Returns
    -------
    bool
        User's input in response to the prompt.
    """
    prompt = ARG_prompt.strip()
    input_hint = __tmp0 (ARG_default)
    _input = formatting.inputwrap (f"{prompt} {input_hint}")
    _input = _input.strip()

    if _input == "":
        return ARG_default
    elif any (re.match (pattern, _input) for pattern in REGEXES_YES):
        return True
    elif any (re.match (pattern, _input) for pattern in REGEXES_NO):
        return False
    else:
        messages.unrecognized_input_message (_input)
        recursive_result = prompt_yesno (ARG_prompt)
        return recursive_result

# ---------- Menus ----------
def _menu_from_options(ARG_menuoptions, ARG_returns_to: str):
    """Displays a menu from a list or tuple of options. Unlike a menu from a dict (see '_menu_from_keyed_options()'), this menu will have automatically assigned 'keys'. The 'ARG_returns_to' is the 'parent' menu, and is always offered as the '0' option.

    Parameters
    ----------
    ARG_menuoptions : list or tuple
        The options to list in the menu display.
    ARG_returns_to : str
        The menu to return to if the user enters '0'.
    """
    assert isinstance (ARG_menuoptions, (list, tuple))
    formatting.printwrap (f"0. {ARG_returns_to}", ARG_indented=True)
    for option_number, option in enumerate (ARG_menuoptions):
        formatting.printwrap (f"{option_number}. {option}", ARG_indented=True)


def _menu_from_keyed_options (ARG_menuoptions, ARG_returns_to):
    """NOT YET IMPLEMENTED!"""
    raise NotImplementedError("The developer has not yet implemented menus based on dicts yet!")


def menu(ARG_name, ARG_parent_menu_name, ARG_options):
    """Displays a menu of options. Technically, a wrapper function for a bunch of other internal functions that it calls depending on the type of ARG_options.

    Parameters
    ----------
    ARG_name : str
        The name of the menu, to be displayed in a header.
    ARG_parent_menu_name : str
        The name of the menu to return to.
    ARG_options : list or tuple or dict
        A list, tuple, or dict containing the options to display.
    """
    formatting.menu_title (ARG_name)
    if isinstance (ARG_options, (list, tuple)):
        _menu_from_options (ARG_options, ARG_returns_to=ARG_parent_menu_name)
    elif isinstance (ARG_options, __typ0):
        _menu_from_keyed_options (ARG_options, ARG_returns_to=ARG_parent_menu_name)
    else:
        raise TypeError

# ---------- Displays ----------
def display_directory_contents():
    """Displays the contents of a directory. NOT YET IMPLEMENTED!"""
    raise NotImplementedError
