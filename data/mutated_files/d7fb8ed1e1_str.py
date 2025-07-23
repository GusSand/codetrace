
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

from functools import partial

import sublime
import sublime_plugin

from ..anaconda_lib import worker, vagrant
from ..anaconda_lib._typing import Dict, Any


class __typ5(sublime_plugin.WindowCommand):
    """Enable Vagrant on this window/project
    """

    def __tmp3(__tmp1) :
        vagrant_worker = worker.WORKERS.get(sublime.active_window().id())
        if vagrant_worker is not None:
            vagrant_worker.support = True


class __typ3(object):
    """Base class for vagrant commands
    """

    data = None  # type: Dict[str, Any]

    def __init__(__tmp1):
        super(__typ3, __tmp1).__init__()
        __tmp1.view = None  # type: sublime.View

    def print_status(__tmp1, __tmp2) :
        """Print the vagrant command output string into a Sublime Text panel
        """

        vagrant_panel = __tmp1.view.window().create_output_panel(
            'anaconda_vagrant'
        )

        vagrant_panel.set_read_only(False)
        region = sublime.Region(0, vagrant_panel.size())
        vagrant_panel.erase(__tmp2, region)
        vagrant_panel.insert(__tmp2, 0, __tmp1.data.decode('utf8'))
        __tmp1.data = None
        vagrant_panel.set_read_only(True)
        vagrant_panel.show(0)
        __tmp1.view.window().run_command(
            'show_panel', {'panel': 'output.anaconda_vagrant'}
        )

    def prepare_data(__tmp1, data: Dict[str, Any]) :
        """Prepare the returned data and call the given command
        """

        success, out, error = data
        __tmp1.data = error if not success else out
        sublime.active_window().run_command(__tmp1._class_name_to_command())

    def _class_name_to_command(__tmp1):
        """Convert class name to command
        """

        command = []
        for i in range(len(__tmp1.__class__.__name__)):
            c = __tmp1.__class__.__name__[i]
            if i == 0:
                command.append(c.lower())
            elif i > 0 and c.isupper():
                command.append('_')
                command.append(c.lower())
            else:
                command.append(c)

        return ''.join(command)


class AnacondaVagrantStatus(sublime_plugin.TextCommand, __typ3):
    """Check vagrant status for configured project
    """

    data = None  # type: Dict[str, Any]

    def __tmp3(__tmp1, __tmp2) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp4 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            try:
                vagrant.VagrantStatus(
                    __tmp1.prepare_data,
                    __tmp4.get('directory', ''),
                    __tmp4.get('machine', 'default'), True
                )
            except Exception as error:
                print(error)
        else:
            __tmp1.print_status(__tmp2)

    def prepare_data(__tmp1, data) :
        """Prepare the returned data
        """

        success, output = data
        __tmp1.data = output
        sublime.active_window().run_command('anaconda_vagrant_status')


class __typ4(sublime_plugin.TextCommand, __typ3):
    """Execute vagrant init with the given parameters
    """

    def __tmp3(__tmp1, __tmp2) :
        __tmp4 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            __tmp1.view.window().show_input_panel(
                'Directory to init on:', '',
                partial(__tmp1.input_directory, __tmp4), None, None
            )
        else:
            __tmp1.print_status(__tmp2)

    def input_directory(__tmp1, __tmp4, __tmp0: <FILL>) -> None:
        machine = __tmp4.get('machine', 'default')
        vagrant.VagrantInit(__tmp1.prepare_data, __tmp0, machine)


class __typ0(sublime_plugin.TextCommand, __typ3):
    """Execute vagrant up command
    """

    def __tmp3(__tmp1, __tmp2) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp4 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            try:
                machine = __tmp4.get('machine', 'default')
                vagrant.VagrantUp(__tmp1.prepare_data, __tmp4['directory'], machine)
            except Exception as error:
                print(error)
        else:
            __tmp1.print_status(__tmp2)


class __typ1(sublime_plugin.TextCommand, __typ3):
    """Execute vagrant reload command
    """

    def __tmp3(__tmp1, __tmp2) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp4 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            try:
                machine = __tmp4.get('machine', 'default')
                vagrant.VagrantReload(
                    __tmp1.prepare_data, __tmp4['directory'], machine
                )
            except Exception as error:
                print(error)
        else:
            __tmp1.print_status(__tmp2)


class __typ2(sublime_plugin.TextCommand, __typ3):
    """Execute remmote ssh command
    """

    def __tmp3(__tmp1, __tmp2) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp4 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            __tmp1.view.window().show_input_panel(
                'Command to execute:', '',
                partial(__tmp1.input_command, __tmp4), None, None
            )
        else:
            __tmp1.print_status(__tmp2)

    def input_command(__tmp1, __tmp4, command: str) :
        machine = __tmp4.get('machine', 'default')
        vagrant.VagrantSSH(
            __tmp1.prepare_data, __tmp4['directory'], command, machine
        )
