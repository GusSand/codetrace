from typing import Callable
from typing import List

import cmd2


class __typ0(cmd2.Cmd):

    """Parental class menus using cmd2 select."""

    def __init__(__tmp0, title: <FILL>) :
        """Initialize selection menu class.

        Parameters
        ----------
        title : menu title

        """
        cmd2.Cmd.__init__(__tmp0)

        __tmp0._title = title.center(30, "~")

    def __tmp1(__tmp0, programs):
        """Start selection loop.

        Parameters
        ----------
        commands : functions docs
        programs : functions to call

        Returns
        -------
        Call of chosen program

        """
        commands = [i.__doc__ for i in programs]
        commands.append("Back")
        while True:
            __tmp0.poutput(__tmp0._title)
            chosen_command = __tmp0.select(commands)
            if chosen_command == "Back":
                break
            chosen_program = commands.index(chosen_command)
            programs[chosen_program]()
