from typing import TypeAlias
__typ0 : TypeAlias = "bool"
# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# dialogsave.py
# rosevomit.programcli.dialogsave
# ___________________________________________________________________
"""A UI module that contains the dialog for saving files."""
import typing

import core.utilities as ut
from core import logs, tempfiles
from programcli import _dialog, formatting, messages

_SAVE_DIALOG_LOGGER = logs.BaseLogger (__name__)


def __tmp0 (__tmp1: str="") -> __typ0:
    """Asks the user if they want to save ARG_file. Basically a convenient wrapper around prompt_yesno().

    Parameters
    ----------
    ARG_filename : str
        The name of the file that the user will be asked if they want to save.

    Returns
    -------
    bool
        If the user wants to save 'ARG_file", this returns 'True'. Else, 'False'.
    """
    if __tmp1 == "":
        result = _dialog.prompt_yesno ("Do you want to save the results? ")
    else:
        result = _dialog.prompt_yesno (f"Save {__tmp1}? ")
    return result


def __tmp4 (__tmp3: <FILL>) :
    """Asks the user what name they want to save the file under.

    Parameters
    ----------
    ARG_format : str
        Used to generate the file extension as ".ARG_format"

    Returns
    -------
    result : str
        This is the filename entered by the user with the file extension ".ARG_format" added to the end.
"""
    if __tmp3[0] != ".":
        extension = "." + __tmp3
    else:
        extension = __tmp3
    prompt = f"Save the {extension} file as: "
    filename = _dialog.prompt_generic (prompt)
    result = filename + extension
    return result


def proactive(ARG_defaultname: str="file"):
    """Use this function *before* generating data.

    Parameters
    ----------
    ARG_defaultname : str, default is "file"
        The filename to save the data under, assuming the user does not choose another name.

    Returns
    -------
    savebool : bool
        If True, the data should be saved at /saved/'filename'. If False, the data should be saved at /temp/'filename'.
    filename : str
        The filename to save the data under.
    """
    savebool: __typ0
    filename: str

    savebool = _dialog.prompt_yesno ("Do you want to save the data once it is generated? (If you choose not to save the data right now, it still may be available in the /temp directory later. No guarentees, though.)")

    _default_name = ut.setname(ARG_defaultname)
    assert isinstance (savebool, __typ0)
    if savebool is True:
        _input = formatting.inputwrap (f"Do you want to save this file as {_default_name}? Leave blank to accept this name, or enter a name of your choice. You don't need to enter the file extension: ")
        _input = _input.strip()  # Strips all leading or trailing whitespaces
        filename = f"{_input}"
    else:
        filename = _default_name
    return savebool, filename


# TODO: break the following function in to two functions - one where the user can decide if the exiting file should be overwritten, and one to prompt the user for a new name.
def __tmp2(__tmp1) :
    """Use this function when the user tries to save data using a name that already exists.

    Parameters
    ----------
    ARG_filename
        The filename that already exists.

    Returns
    -------
    str (new_filename) or bool
      This function returns 'True' if the user decides to keep the original file and delete the current data without saving it. This function returns 'False' if the user decides to overwrite the original file with the new data. If this function returns a string, this means that the user has decided to save data under a new filename.
    """
    formatting.printwrap (f"A file with the filename 'saved/{__tmp1}' already exists. What should we do with the temporary file 'temp/{__tmp1}'?")
    formatting.printwrap (f"    1. Overwrite the old 'saved/{__tmp1}' using 'temp/{__tmp1}'")
    formatting.printwrap (f"    2. Keep the old 'saved/{__tmp1}' and delete 'temp/{__tmp1}'")
    formatting.printwrap (f"    3. Save 'temp/{__tmp1}' under a new name.")
    _input = input ("Choose an option: ")
    _input = _input.strip()
    if _input == "1":
        return False
    elif _input == "2":
        return True
    elif _input == "3":
        save_as = input ("Enter new name: ")
        save_as = save_as.strip()
        if save_as == "":
            new_filename = "new-" + __tmp1
        return new_filename
    else:
        messages.unrecognized_input_message (_input)
        recursive_result = __tmp2(__tmp1)
        return recursive_result
