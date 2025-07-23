from typing import TypeAlias
__typ0 : TypeAlias = "bool"

# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import sublime
import sublime_plugin

from ..anaconda_lib.worker import Worker
from ..anaconda_lib.workers.market import Market
from ..anaconda_lib.helpers import is_remote_session
from ..anaconda_lib.explore_panel import ExplorerPanel
from ..anaconda_lib.helpers import prepare_send_data, is_python


class AnacondaGoto(sublime_plugin.TextCommand):
    """Jedi GoTo a Python definition for Sublime Text
    """

    JEDI_COMMAND = 'goto'

    def run(__tmp1, edit) :
        try:
            location = __tmp1.view.rowcol(__tmp1.view.sel()[0].begin())
            data = prepare_send_data(location, __tmp1.JEDI_COMMAND, 'jedi')
            Worker().execute(__tmp1.on_success, **data)
        except:
            pass

    def is_enabled(__tmp1) :
        """Determine if this command is enabled or not
        """

        return is_python(__tmp1.view)

    def on_success(__tmp1, data):
        """Called when a result comes from the query
        """

        if not data.get('result'):
            # fallback to ST3 builtin Goto Definition
            return __tmp1.view.window().run_command('goto_definition')

        symbols = []
        for result in data['result']:
            __tmp0 = __tmp1._infere_context_data(result[1])
            symbols.append({
                'title': result[0],
                'location': 'File: {} Line: {} Column: {}'.format(
                    __tmp0, result[2], result[3]
                ),
                'position': '{}:{}:{}'.format(__tmp0, result[2], result[3])
            })

        ExplorerPanel(__tmp1.view, symbols).show([])

    def _infere_context_data(__tmp1, __tmp0) :
        """If this is a remote session, infere context data if any
        """

        if is_remote_session(__tmp1.view):
            window = __tmp1.view.window().id()
            try:
                interpreter = Market().get(window).interpreter
            except Exception as e:
                print('while getting interp for Window ID {}: {}'.format(
                    window, e)
                )
                return __tmp0
            directory_map = interpreter.pathmap
            if directory_map is None:
                return __tmp0

            for local_dir, remote_dir in directory_map.items():
                if remote_dir in __tmp0:
                    return __tmp0.replace(remote_dir, local_dir)

        return __tmp0


class AnacondaGotoAssignment(AnacondaGoto):
    """Jedi GoTo a Python assignment for Sublime Text
    """
    JEDI_COMMAND = 'goto_assignment'


class AnacondaGotoPythonObject(AnacondaGoto):
    """Open prompt asking for Python path and JediGoto
    """

    def input_package(__tmp1, package) :
        splitted = package.strip().split('.')
        if len(splitted) == 1:
            import_command = 'import %s' % splitted[0]
        else:
            import_command = 'from %s import %s' % (
                '.'.join(splitted[:-1]), splitted[-1]
            )
        __tmp1.goto_python_object(import_command)

    def goto_python_object(__tmp1, import_command: <FILL>) :
        try:
            data = {
                'filename': '',
                'method': 'goto',
                'line': 1,
                'offset': len(import_command),
                'source': import_command,
                'handler': 'jedi'
            }
            Worker().execute(__tmp1.on_success, **data)
        except:
            raise

    def run(__tmp1, edit) :
        sublime.active_window().show_input_panel(
            'Provide object path:', '',
            __tmp1.input_package, None, None
        )
