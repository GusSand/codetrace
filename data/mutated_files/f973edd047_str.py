
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

from functools import partial

import sublime
import sublime_plugin

from ..anaconda_lib import worker, vagrant
from ..anaconda_lib._typing import Dict, Any


class __typ6(sublime_plugin.WindowCommand):
    """Enable Vagrant on this window/project
    """

    def __tmp4(__tmp1) -> None:
        vagrant_worker = worker.WORKERS.get(sublime.active_window().id())
        if vagrant_worker is not None:
            vagrant_worker.support = True


class __typ4(object):
    """Base class for vagrant commands
    """

    data = None  # type: Dict[str, Any]

    def __init__(__tmp1):
        super(__typ4, __tmp1).__init__()
        __tmp1.view = None  # type: sublime.View

    def print_status(__tmp1, __tmp3) -> None:
        """Print the vagrant command output string into a Sublime Text panel
        """

        vagrant_panel = __tmp1.view.window().create_output_panel(
            'anaconda_vagrant'
        )

        vagrant_panel.set_read_only(False)
        region = sublime.Region(0, vagrant_panel.size())
        vagrant_panel.erase(__tmp3, region)
        vagrant_panel.insert(__tmp3, 0, __tmp1.data.decode('utf8'))
        __tmp1.data = None
        vagrant_panel.set_read_only(True)
        vagrant_panel.show(0)
        __tmp1.view.window().run_command(
            'show_panel', {'panel': 'output.anaconda_vagrant'}
        )

    def prepare_data(__tmp1, data) :
        """Prepare the returned data and call the given command
        """

        success, out, error = data
        __tmp1.data = error if not success else out
        sublime.active_window().run_command(__tmp1._class_name_to_command())

    def _class_name_to_command(__tmp1):
        """Convert class name to command
        """

        __tmp2 = []
        for i in range(len(__tmp1.__class__.__name__)):
            c = __tmp1.__class__.__name__[i]
            if i == 0:
                __tmp2.append(c.lower())
            elif i > 0 and c.isupper():
                __tmp2.append('_')
                __tmp2.append(c.lower())
            else:
                __tmp2.append(c)

        return ''.join(__tmp2)


class __typ3(sublime_plugin.TextCommand, __typ4):
    """Check vagrant status for configured project
    """

    data = None  # type: Dict[str, Any]

    def __tmp4(__tmp1, __tmp3) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp5 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            try:
                vagrant.VagrantStatus(
                    __tmp1.prepare_data,
                    __tmp5.get('directory', ''),
                    __tmp5.get('machine', 'default'), True
                )
            except Exception as error:
                print(error)
        else:
            __tmp1.print_status(__tmp3)

    def prepare_data(__tmp1, data) :
        """Prepare the returned data
        """

        success, output = data
        __tmp1.data = output
        sublime.active_window().run_command('anaconda_vagrant_status')


class __typ5(sublime_plugin.TextCommand, __typ4):
    """Execute vagrant init with the given parameters
    """

    def __tmp4(__tmp1, __tmp3) -> None:
        __tmp5 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            __tmp1.view.window().show_input_panel(
                'Directory to init on:', '',
                partial(__tmp1.input_directory, __tmp5), None, None
            )
        else:
            __tmp1.print_status(__tmp3)

    def input_directory(__tmp1, __tmp5: Dict[str, Any], __tmp0) -> None:
        machine = __tmp5.get('machine', 'default')
        vagrant.VagrantInit(__tmp1.prepare_data, __tmp0, machine)


class __typ0(sublime_plugin.TextCommand, __typ4):
    """Execute vagrant up command
    """

    def __tmp4(__tmp1, __tmp3) -> None:
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp5 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            try:
                machine = __tmp5.get('machine', 'default')
                vagrant.VagrantUp(__tmp1.prepare_data, __tmp5['directory'], machine)
            except Exception as error:
                print(error)
        else:
            __tmp1.print_status(__tmp3)


class __typ2(sublime_plugin.TextCommand, __typ4):
    """Execute vagrant reload command
    """

    def __tmp4(__tmp1, __tmp3) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp5 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            try:
                machine = __tmp5.get('machine', 'default')
                vagrant.VagrantReload(
                    __tmp1.prepare_data, __tmp5['directory'], machine
                )
            except Exception as error:
                print(error)
        else:
            __tmp1.print_status(__tmp3)


class __typ1(sublime_plugin.TextCommand, __typ4):
    """Execute remmote ssh command
    """

    def __tmp4(__tmp1, __tmp3) :
        if __tmp1.view.settings().get('vagrant_environment') is None:
            return

        __tmp5 = __tmp1.view.settings().get('vagrant_environment')
        if __tmp1.data is None:
            __tmp1.view.window().show_input_panel(
                'Command to execute:', '',
                partial(__tmp1.input_command, __tmp5), None, None
            )
        else:
            __tmp1.print_status(__tmp3)

    def input_command(__tmp1, __tmp5, __tmp2: <FILL>) -> None:
        machine = __tmp5.get('machine', 'default')
        vagrant.VagrantSSH(
            __tmp1.prepare_data, __tmp5['directory'], __tmp2, machine
        )
