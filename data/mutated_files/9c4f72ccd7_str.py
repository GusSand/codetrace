from typing import TypeAlias
__typ0 : TypeAlias = "int"
# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# logiccontroller.py
# rosevomit.programlogic.logiccontroller
# ___________________________________________________________________
"""This is the main "logic" file. Its job is to keep track of the program's custom logic modules and to serve as an intermediary in between them and the main file (rosevomit.py). This isn't actually necessary, but it serves as good coding practice for me. Hopefully."""
import datetime
import os
import textwrap

try:
    from core import logs, customerrors, constants
    import core.utilities as ut
    from programcli import dialogsave
    from programlogic import suncalc, randomevent, randomname
except ImportError:
    from rosevomit.core import logs, customerrors, constants
    import rosevomit.core.utilities as ut
    from rosevomit.programcli import dialogsave
    from rosevomit.programlogic import suncalc, randomevent, randomname


_LOGICLOGGER = logs.BaseLogger (__name__)


def __tmp7 (__tmp3: <FILL>, __tmp10):
    """This function generates a number of random names.

    Parameters
    ----------
    ARG_nametype : str
        Valid nametypes are 'first', 'firstfemale', 'firstmale', 'last', 'full', 'fullfemale', 'fullmale'.
    ARG_number : int
        The number of names to generate.
    """
    if __tmp3 == "first":
        ut.repeat (randomname.getname_firstany, __tmp10)
    elif __tmp3 == "firstfemale":
        ut.repeat (randomname.getname_firstfemale, __tmp10)
    elif __tmp3 == "firstmale":
        ut.repeat (randomname.getname_firstmale, __tmp10)
    elif __tmp3 == "last":
        ut.repeat (randomname.getname_lastany, __tmp10)
    elif __tmp3 == "full":
        ut.repeat (randomname.getname_fullany, __tmp10)
    elif __tmp3 == "fullfemale":
        ut.repeat (randomname.getname_fullfemale, __tmp10)
    elif __tmp3 == "fullmale":
        ut.repeat (randomname.getname_fullmale, __tmp10)
    else:
        raise ValueError ("rosevomit.programlogic.logiccontroller.generatenames() encountered an unexpected value for 'ARG_nametype'. The value of ARG_nametype was: {}".format(__tmp3))


def __tmp0(__tmp6: str, __tmp9):
    """This function receives the user input and calls functions accordingly.

    Parameters
    ----------
    ARG_eventtypes : str
        The only valid eventtype at the moment is 'globalevents'.
    ARG_yearrange : int
        The number of years to generate events for.
    """
    if __tmp6 == "globalevents":
        def __tmp5(__tmp2, __tmp4):
            """This function checks to see what events have happened in a given year. It assumes that the probability of events does not change from year to year."""
            events = []
            print (f"{__tmp2} years ago, scholars tell us...")
            # Run checks to generate events. The randomevent checks return a list whose elements are the event text of events that occured. We add these elements to the "events" list.
            events.extend (randomevent.check_volcano (__tmp2, __tmp4))
            events.extend (randomevent.check_earthquake (__tmp2, __tmp4))
            events.extend (randomevent.check_impact (__tmp2, __tmp4))
            events.extend (randomevent.check_astronomy (__tmp2, __tmp4))
            for item in range (len (events)):
                print (textwrap.fill (f"    {events[item]}", width=70))
                print ()

        try:
            try:
                os.chdir ("./temp/")
            except FileNotFoundError:
                os.chdir ("..")
                os.chdir ("./temp")
        except FileNotFoundError:  # Maybe it's being run by a testing script?
            os.chdir ("..")
            os.chdir ("./rosevomit/temp/")
        _tempfile_name = ut.setname("timeline")
        _tempfile = open(_tempfile_name, "a+")

        _this_year = __tmp9
        for item in range (0, __tmp9):
            __tmp5 (__tmp2=_this_year, __tmp4=_tempfile_name)
            _this_year = (_this_year - 1)

        _tempfile.write ("Testing.")
        _tempfile.close()
    else:
        raise ValueError ("rosevomit.programlogic.logiccontroller.gen_timeline() encountered an unexpected value for 'ARG_eventtypes'. The value of ARG_eventtypes was: {}".format(__tmp6))


def __tmp8 (__tmp1, __tmp11):
    """Calls the suncalc function

    Parameters
    ----------
    ARG_lat, ARG_long
        The observer's latitude and longitude, which will be passed to suncalc.main()
    """
    os.chdir (constants.SAVE_DIRECTORY_PATH)
    current_time = datetime.datetime.now()
    datestring = current_time.strftime ("%Y%b%d-%H%M")
    filename_for_results = "suncalc_" + datestring
    suncalc.main (__tmp1, __tmp11, __tmp4=filename_for_results)
