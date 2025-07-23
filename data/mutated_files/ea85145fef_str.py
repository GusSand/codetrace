
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

from functools import partial

import sublime
import sublime_plugin

from ..anaconda_lib import worker, vagrant
from ..anaconda_lib.typing import Dict, Any


class AnacondaVagrantEnable(sublime_plugin.WindowCommand):
    """Enable Vagrant on this window/project
    """

    def run(self) :
        vagrant_worker = worker.WORKERS.get(sublime.active_window().id())
        if vagrant_worker is not None:
            vagrant_worker.support = True


class __typ0(object):
    """Base class for vagrant commands
    """

    data = None  # type: Dict[str, Any]

    def __init__(self):
        super(__typ0, self).__init__()
        self.view = None  # type: sublime.View

    def print_status(self, __tmp1: sublime.Edit) :
        """Print the vagrant command output string into a Sublime Text panel
        """

        vagrant_panel = self.view.window().create_output_panel(
            'anaconda_vagrant'
        )

        vagrant_panel.set_read_only(False)
        region = sublime.Region(0, vagrant_panel.size())
        vagrant_panel.erase(__tmp1, region)
        vagrant_panel.insert(__tmp1, 0, self.data.decode('utf8'))
        self.data = None
        vagrant_panel.set_read_only(True)
        vagrant_panel.show(0)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.anaconda_vagrant'}
        )

    def prepare_data(self, data) -> None:
        """Prepare the returned data and call the given command
        """

        success, out, error = data
        self.data = error if not success else out
        sublime.active_window().run_command(self._class_name_to_command())

    def _class_name_to_command(self):
        """Convert class name to command
        """

        __tmp0 = []
        for i in range(len(self.__class__.__name__)):
            c = self.__class__.__name__[i]
            if i == 0:
                __tmp0.append(c.lower())
            elif i > 0 and c.isupper():
                __tmp0.append('_')
                __tmp0.append(c.lower())
            else:
                __tmp0.append(c)

        return ''.join(__tmp0)


class AnacondaVagrantStatus(sublime_plugin.TextCommand, __typ0):
    """Check vagrant status for configured project
    """

    data = None  # type: Dict[str, Any]

    def run(self, __tmp1) :
        if self.view.settings().get('vagrant_environment') is None:
            return

        __tmp2 = self.view.settings().get('vagrant_environment')
        if self.data is None:
            try:
                vagrant.VagrantStatus(
                    self.prepare_data,
                    __tmp2.get('directory', ''),
                    __tmp2.get('machine', 'default'), True
                )
            except Exception as error:
                print(error)
        else:
            self.print_status(__tmp1)

    def prepare_data(self, data) -> None:
        """Prepare the returned data
        """

        success, output = data
        self.data = output
        sublime.active_window().run_command('anaconda_vagrant_status')


class AnacondaVagrantInit(sublime_plugin.TextCommand, __typ0):
    """Execute vagrant init with the given parameters
    """

    def run(self, __tmp1: sublime.Edit) -> None:
        __tmp2 = self.view.settings().get('vagrant_environment')
        if self.data is None:
            self.view.window().show_input_panel(
                'Directory to init on:', '',
                partial(self.input_directory, __tmp2), None, None
            )
        else:
            self.print_status(__tmp1)

    def input_directory(self, __tmp2, directory: str) :
        machine = __tmp2.get('machine', 'default')
        vagrant.VagrantInit(self.prepare_data, directory, machine)


class AnacondaVagrantUp(sublime_plugin.TextCommand, __typ0):
    """Execute vagrant up command
    """

    def run(self, __tmp1: sublime.Edit) :
        if self.view.settings().get('vagrant_environment') is None:
            return

        __tmp2 = self.view.settings().get('vagrant_environment')
        if self.data is None:
            try:
                machine = __tmp2.get('machine', 'default')
                vagrant.VagrantUp(self.prepare_data, __tmp2['directory'], machine)
            except Exception as error:
                print(error)
        else:
            self.print_status(__tmp1)


class AnacondaVagrantReload(sublime_plugin.TextCommand, __typ0):
    """Execute vagrant reload command
    """

    def run(self, __tmp1) -> None:
        if self.view.settings().get('vagrant_environment') is None:
            return

        __tmp2 = self.view.settings().get('vagrant_environment')
        if self.data is None:
            try:
                machine = __tmp2.get('machine', 'default')
                vagrant.VagrantReload(
                    self.prepare_data, __tmp2['directory'], machine
                )
            except Exception as error:
                print(error)
        else:
            self.print_status(__tmp1)


class AnacondaVagrantSsh(sublime_plugin.TextCommand, __typ0):
    """Execute remmote ssh command
    """

    def run(self, __tmp1: sublime.Edit) -> None:
        if self.view.settings().get('vagrant_environment') is None:
            return

        __tmp2 = self.view.settings().get('vagrant_environment')
        if self.data is None:
            self.view.window().show_input_panel(
                'Command to execute:', '',
                partial(self.input_command, __tmp2), None, None
            )
        else:
            self.print_status(__tmp1)

    def input_command(self, __tmp2: Dict[str, Any], __tmp0: <FILL>) :
        machine = __tmp2.get('machine', 'default')
        vagrant.VagrantSSH(
            self.prepare_data, __tmp2['directory'], __tmp0, machine
        )
