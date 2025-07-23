from typing import TypeAlias
__typ1 : TypeAlias = "dict"
__typ0 : TypeAlias = "str"
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
def _prompt_hint_bool (ARG_default: <FILL>) :
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


def __tmp4 (__tmp1) -> __typ0:
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
    _input = formatting.inputwrap (__tmp1)
    result = _input.strip()
    if result == "":
        messages.unrecognized_input_message (result)
        recursive_result = __tmp4 (__tmp1)
        result = recursive_result
    return result


def __tmp0 (__tmp1, ARG_default: bool=True) :
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
    prompt = __tmp1.strip()
    input_hint = _prompt_hint_bool (ARG_default)
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
        recursive_result = __tmp0 (__tmp1)
        return recursive_result

# ---------- Menus ----------
def __tmp3(__tmp8, ARG_returns_to):
    """Displays a menu from a list or tuple of options. Unlike a menu from a dict (see '_menu_from_keyed_options()'), this menu will have automatically assigned 'keys'. The 'ARG_returns_to' is the 'parent' menu, and is always offered as the '0' option.

    Parameters
    ----------
    ARG_menuoptions : list or tuple
        The options to list in the menu display.
    ARG_returns_to : str
        The menu to return to if the user enters '0'.
    """
    assert isinstance (__tmp8, (list, tuple))
    formatting.printwrap (f"0. {ARG_returns_to}", ARG_indented=True)
    for option_number, option in enumerate (__tmp8):
        formatting.printwrap (f"{option_number}. {option}", ARG_indented=True)


def __tmp6 (__tmp8, ARG_returns_to):
    """NOT YET IMPLEMENTED!"""
    raise NotImplementedError("The developer has not yet implemented menus based on dicts yet!")


def __tmp2(__tmp5: __typ0, ARG_parent_menu_name: __typ0, __tmp7: Union[list, tuple, __typ1]):
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
    formatting.menu_title (__tmp5)
    if isinstance (__tmp7, (list, tuple)):
        __tmp3 (__tmp7, ARG_returns_to=ARG_parent_menu_name)
    elif isinstance (__tmp7, __typ1):
        __tmp6 (__tmp7, ARG_returns_to=ARG_parent_menu_name)
    else:
        raise TypeError

# ---------- Displays ----------
def display_directory_contents():
    """Displays the contents of a directory. NOT YET IMPLEMENTED!"""
    raise NotImplementedError
