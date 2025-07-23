# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# messages.py
# rosevomit.programcli.messages
# ___________________________________________________________________
"""Contains system messages to display to users."""
from core import about, logs
from programcli import formatting

_MESSAGE_LOGGER = logs.BaseLogger (__name__)

# ---------- Standard messages ----------
def general_program_message (__tmp4: <FILL>):
    """A generic message. Displays a textwrapped message, and then 'Press Enter to Continue.' The user can then press enter.

    Parameters
    ----------
    ARG_string : str
        The message contents to display.
    """
    print ()
    formatting.printwrap (f"{__tmp4} Press 'Enter' to continue.")
    input()


def unrecognized_input_message (ARG_input):
    """Displays a message saying 'Sorry, ARG_input isn't a recognized command in this menu/dialog.'
    
    Parameters
    ----------
    ARG_input
        The input that was not recognized.
    """
    formatting.printwrap (f"Sorry, {ARG_input} isn't a recognized in this menu/dialog.")
    print ()

# ---------- Warnings ----------
def __tmp0 (__tmp2, __tmp1, __tmp3):
    """Displays a warning that this version is pre-release version.

    Parameters
    ----------
    ARG_major_version, ARG_minor_version, ARG_patch_version
        The components of the current version number.
    """
    formatting.printwrap (f"You are using Rosevomit version {__tmp2}.{__tmp1}.{__tmp3}. This software is actively under development. Proceed at your own risk.")


def warning_version_is_devbuild ():
    """Displays a warning that this version is a development build for a version past 1.0. For prerelease devbuilds, use 'warning_version_is_prerelease_devbuild()'.

    NOT CURRENTLY USED.
    """
    # Will be written once we hit version 1.0
    raise NotImplementedError


def warning_version_is_prerelease_devbuild (__tmp2, __tmp1, __tmp3):
    """Displays a warning that this version is both a pre-release version and a development build.

    Parameters
    ----------
    ARG_major_version, ARG_minor_version, ARG_patch_version
        The components of the current version number.
    """
    formatting.printwrap (f"You are using a development build of Rosevomit {__tmp2}.{__tmp1}.{__tmp3}. This software is actively under development, and this development build may not be stable! Proceed at your own risk.")

# ---------- "About" messages ----------
def about_license_message():
    """Displays the strings contained in rosevomit.core.about.LICENSE. Accepts no parameters, returns nothing."""
    print()
    for string in about.LICENSE:
        formatting.printwrap (string)
        print()
    general_program_message("   ")
    print()


def about_program_message():
    """Displays the strings contained in rosevomit.core.about.PROGRAM. Accepts no parameters, returns nothing."""
    print()
    for string in about.PROGRAM:
        formatting.printwrap (string)
        print()
    general_program_message("   ")
    print()
