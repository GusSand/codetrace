# This Python file uses the following encoding: utf-8
# ___________________________________________________________________
# logs.py
# rosevomit.core.logs
# ___________________________________________________________________
"""This file contains config dictionaries for the default logger."""
import datetime
import logging
import logging.handlers
import os


class __typ0:  # pylint: disable=too-few-public-methods
    """Auxiliary logger, which can be called from other modules.

    Upon __init__, creates a logger with ARG_loggername as a name and generates a INFO-level log record saying 'Logger initialized.'.

    Parameters
    ----------
    ARG_loggername : str
        The name that the logger should be called under. It's highly recommended to just set ARG_loggername to __name__.
    """
    def __init__(self, ARG_loggername: <FILL>):
        self.logger = logging.getLogger (f"{ARG_loggername}")
        self.logger.info ("Logger initialized.")

_LOGALOG = __typ0(__name__)

from core import settings
from core.constants import LOG_DIRECTORY_PATH

def _startsession (ARG_targetfile):
    """Writes a blank line and a session header to the targetfile.

    Parameters
    ----------
    ARG_targetfile : any type that open() accepts as a filename
        Path to the file that should recieve the new session header.
    """
    if os.path.isfile(ARG_targetfile) is False:
        fileheader = _logfile_readme()
        with open(ARG_targetfile, "w") as f:
            f.write (fileheader)
    with open(ARG_targetfile, "a") as f:
        t_start = datetime.datetime.now()
        f.write(f"\n---------- BEGIN SESSION: {t_start} ----------\n")


def _logfile_readme() :
    """Returns a string containing a 'how to read this logfile' message.

    Returns
    -------
    str
        Returns a formatted paragraph-long message with tips on reading log file output.
    """
    line1 = "Messages are displayed below in the format"
    line2 = "    <DATE> <TIME> <LOGGER NAME> @ <FILE>:<LINE> - <LEVEL> - <FUNCTION>:<MESSAGE>"
    line3 = "where <DATE> is the date in 'YYYY-MM-DD' format, <TIME> is the time in 'HH:MM:SS,milliseconds' format, <LOGGER NAME> is the name of the logger that generated the message (which should be the __name__ of the file where the logger was initialized), <FILE> and <LINE> is the file name and line number where the message was generated, <LEVEL> is the priority level that the message was generated at, <FUNCTION> is the name of the function that the message was generated inside, and <MESSAGE> is the actual message that was generated. "
    message = f"{line1}\n\n{line2}\n\n{line3}\n\n"
    return message


def start_logging(ARG_parentlogger, __tmp0):
    """Create file handlers, creates formatter and adds it to the handlers, and adds those handlers to logger.

    Parameters
    ----------
    ARG_parentlogger : logging.Logger
        The root logger.
    ARG_bufferlogger : logging.handlers.Memoryhandler
        A MemoryHander object to buffer messages to.
    """
    if settings.logging_service() is False:
        pass
    else:
        filehandlers = []

        debugfile = os.path.join (LOG_DIRECTORY_PATH, "10-debug.log")
        _startsession (debugfile)
        filehandler1 = logging.FileHandler(debugfile)
        filehandler1.setLevel (logging.DEBUG)
        filehandlers.append (filehandler1)

        infofile = os.path.join (LOG_DIRECTORY_PATH, "20-info.log")
        _startsession (infofile)
        filehandler2 = logging.FileHandler(infofile)
        filehandler2.setLevel (logging.INFO)
        filehandlers.append (filehandler2)

        warnfile = os.path.join (LOG_DIRECTORY_PATH, "30-warning.log")
        _startsession (warnfile)
        filehandler3 = logging.FileHandler(warnfile)
        filehandler3.setLevel (logging.WARNING)
        filehandlers.append (filehandler3)

        errorfile = os.path.join (LOG_DIRECTORY_PATH, "40-error.log")
        _startsession (errorfile)
        filehandler4 = logging.FileHandler(errorfile)
        filehandler4.setLevel (logging.ERROR)
        filehandlers.append (filehandler4)

        criticalfile = os.path.join (LOG_DIRECTORY_PATH, "50-critical.log")
        _startsession (criticalfile)
        filehandler5 = logging.FileHandler(criticalfile)
        filehandler5.setLevel (logging.CRITICAL)
        filehandlers.append (filehandler5)

        formatter = logging.Formatter ("%(asctime)s %(name)s @ %(filename)s:%(lineno)d - %(levelname)s - %(funcName)s: %(message)s")
        for item in filehandlers:
            item.setFormatter (formatter)
            ARG_parentlogger.addHandler (item)

        bufferfile = os.path.join (LOG_DIRECTORY_PATH, "00-buffer.log")
        _startsession (bufferfile)
        bufferfilehandler = logging.FileHandler(bufferfile)
        bufferfilehandler.setFormatter(formatter)

        __tmp0.setTarget(bufferfilehandler)
        __tmp0.flush()
        __tmp0.close()
