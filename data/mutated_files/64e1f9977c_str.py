
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

from functools import partial

import sublime
import sublime_plugin

from ..anaconda_lib import worker, vagrant
from ..anaconda_lib._typing import Dict, Any


class AnacondaVagrantEnable(sublime_plugin.WindowCommand):
    """Enable Vagrant on this window/project
    """

    def __tmp2(__tmp0) :
        vagrant_worker = worker.WORKERS.get(sublime.active_window().id())
        if vagrant_worker is not None:
            vagrant_worker.support = True


class __typ1(object):
    """Base class for vagrant commands
    """

    data = None  # type: Dict[str, Any]

    def __init__(__tmp0):
        super(__typ1, __tmp0).__init__()
        __tmp0.view = None  # type: sublime.View

    def print_status(__tmp0, __tmp1) :
        """Print the vagrant command output string into a Sublime Text panel
        """

        vagrant_panel = __tmp0.view.window().create_output_panel(
            'anaconda_vagrant'
        )

        vagrant_panel.set_read_only(False)
        region = sublime.Region(0, vagrant_panel.size())
        vagrant_panel.erase(__tmp1, region)
        vagrant_panel.insert(__tmp1, 0, __tmp0.data.decode('utf8'))
        __tmp0.data = None
        vagrant_panel.set_read_only(True)
        vagrant_panel.show(0)
        __tmp0.view.window().run_command(
            'show_panel', {'panel': 'output.anaconda_vagrant'}
        )

    def prepare_data(__tmp0, data) :
        """Prepare the returned data and call the given command
        """

        success, out, error = data
        __tmp0.data = error if not success else out
        sublime.active_window().run_command(__tmp0._class_name_to_command())

    def _class_name_to_command(__tmp0):
        """Convert class name to command
        """

        command = []
        for i in range(len(__tmp0.__class__.__name__)):
            c = __tmp0.__class__.__name__[i]
            if i == 0:
                command.append(c.lower())
            elif i > 0 and c.isupper():
                command.append('_')
                command.append(c.lower())
            else:
                command.append(c)

        return ''.join(command)


class AnacondaVagrantStatus(sublime_plugin.TextCommand, __typ1):
    """Check vagrant status for configured project
    """

    data = None  # type: Dict[str, Any]

    def __tmp2(__tmp0, __tmp1: sublime.Edit) -> None:
        if __tmp0.view.settings().get('vagrant_environment') is None:
            return

        __tmp3 = __tmp0.view.settings().get('vagrant_environment')
        if __tmp0.data is None:
            try:
                vagrant.VagrantStatus(
                    __tmp0.prepare_data,
                    __tmp3.get('directory', ''),
                    __tmp3.get('machine', 'default'), True
                )
            except Exception as error:
                print(error)
        else:
            __tmp0.print_status(__tmp1)

    def prepare_data(__tmp0, data: Dict[str, Any]) :
        """Prepare the returned data
        """

        success, output = data
        __tmp0.data = output
        sublime.active_window().run_command('anaconda_vagrant_status')


class AnacondaVagrantInit(sublime_plugin.TextCommand, __typ1):
    """Execute vagrant init with the given parameters
    """

    def __tmp2(__tmp0, __tmp1) :
        __tmp3 = __tmp0.view.settings().get('vagrant_environment')
        if __tmp0.data is None:
            __tmp0.view.window().show_input_panel(
                'Directory to init on:', '',
                partial(__tmp0.input_directory, __tmp3), None, None
            )
        else:
            __tmp0.print_status(__tmp1)

    def input_directory(__tmp0, __tmp3, directory: <FILL>) :
        machine = __tmp3.get('machine', 'default')
        vagrant.VagrantInit(__tmp0.prepare_data, directory, machine)


class __typ0(sublime_plugin.TextCommand, __typ1):
    """Execute vagrant up command
    """

    def __tmp2(__tmp0, __tmp1) :
        if __tmp0.view.settings().get('vagrant_environment') is None:
            return

        __tmp3 = __tmp0.view.settings().get('vagrant_environment')
        if __tmp0.data is None:
            try:
                machine = __tmp3.get('machine', 'default')
                vagrant.VagrantUp(__tmp0.prepare_data, __tmp3['directory'], machine)
            except Exception as error:
                print(error)
        else:
            __tmp0.print_status(__tmp1)


class AnacondaVagrantReload(sublime_plugin.TextCommand, __typ1):
    """Execute vagrant reload command
    """

    def __tmp2(__tmp0, __tmp1) :
        if __tmp0.view.settings().get('vagrant_environment') is None:
            return

        __tmp3 = __tmp0.view.settings().get('vagrant_environment')
        if __tmp0.data is None:
            try:
                machine = __tmp3.get('machine', 'default')
                vagrant.VagrantReload(
                    __tmp0.prepare_data, __tmp3['directory'], machine
                )
            except Exception as error:
                print(error)
        else:
            __tmp0.print_status(__tmp1)


class AnacondaVagrantSsh(sublime_plugin.TextCommand, __typ1):
    """Execute remmote ssh command
    """

    def __tmp2(__tmp0, __tmp1) -> None:
        if __tmp0.view.settings().get('vagrant_environment') is None:
            return

        __tmp3 = __tmp0.view.settings().get('vagrant_environment')
        if __tmp0.data is None:
            __tmp0.view.window().show_input_panel(
                'Command to execute:', '',
                partial(__tmp0.input_command, __tmp3), None, None
            )
        else:
            __tmp0.print_status(__tmp1)

    def input_command(__tmp0, __tmp3: Dict[str, Any], command) :
        machine = __tmp3.get('machine', 'default')
        vagrant.VagrantSSH(
            __tmp0.prepare_data, __tmp3['directory'], command, machine
        )
