# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# antikythera_time.py
# rosevomit.programlogic.antikythera_time
# ___________________________________________________________________
"""A file containing functions related to Antikythera's date/time/calendars."""
from decimal import Decimal

from core import logs
from core.utilities import validate_range


_TIMETRACKER = logs.BaseLogger (__name__)


def __tmp0 (ARG_day: <FILL>, ARG_hour: int=0, ARG_minute: int=0, ARG_second: int=0):
    """This function accepts arguments for a given time (day, hour, minute, and second) of the year, and returns the equivalent fractional day.

    Parameters
    ----------
    ARG_day : int
        The day of the year of the desired fractional date, from 1 to 365.
    ARG_hour, ARG_minute, ARG_second : int (default is 0)
        The hour, minute, and second of the desired fractional date. 'ARG_hour' must be between 0 and 23. 'ARG_minute' and 'ARG_second' must be between 0 and 59.

    Returns
    -------
    int or Decimal
        The fractional day equivalent to the given day, hour, minute, and second.
    """
    arglist = [ARG_day, ARG_hour, ARG_minute, ARG_second]
    for arg in arglist:
        assert isinstance (arg, int)
    validate_range (ARG_day, 1, 365, ARG_raise_ex=True)
    validate_range (ARG_hour, 0, 23, ARG_raise_ex=True)
    validate_range (ARG_minute, 0, 59, ARG_raise_ex=True)
    validate_range (ARG_second, 0, 59, ARG_raise_ex=True)
    # Adjusting the day to a "0th count day"
    day_0_count = ARG_day - 1
    result = day_0_count + Decimal(f"{ARG_hour / 24}") + Decimal(f"{ARG_minute / 1440}") + Decimal(f"{ARG_second / 86400}")
    return result
