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

    def __tmp4(__tmp0, __tmp3: sublime.Edit) :
        try:
            location = __tmp0.view.rowcol(__tmp0.view.sel()[0].begin())
            data = prepare_send_data(location, __tmp0.JEDI_COMMAND, 'jedi')
            Worker().execute(__tmp0.on_success, **data)
        except:
            pass

    def __tmp1(__tmp0) :
        """Determine if this command is enabled or not
        """

        return is_python(__tmp0.view)

    def on_success(__tmp0, data):
        """Called when a result comes from the query
        """

        if not data['result']:
            # fallback to ST3 builtin Goto Definition
            return __tmp0.view.window().run_command('goto_definition')

        symbols = []
        for result in data['result']:
            path = __tmp0._infere_context_data(result[1])
            symbols.append({
                'title': result[0],
                'location': 'File: {} Line: {} Column: {}'.format(
                    path, result[2], result[3]
                ),
                'position': '{}:{}:{}'.format(path, result[2], result[3])
            })

        ExplorerPanel(__tmp0.view, symbols).show([])

    def _infere_context_data(__tmp0, path: <FILL>) -> str:
        """If this is a remote session, infere context data if any
        """

        if is_remote_session(__tmp0.view):
            window = __tmp0.view.window().id()
            try:
                interpreter = Market().get(window).interpreter
            except Exception as e:
                print('while getting interp for Window ID {}: {}'.format(
                    window, e)
                )
                return path
            directory_map = interpreter.pathmap
            if directory_map is None:
                return path

            for local_dir, remote_dir in directory_map.items():
                if remote_dir in path:
                    return path.replace(remote_dir, local_dir)

        return path


class __typ1(AnacondaGoto):
    """Jedi GoTo a Python assignment for Sublime Text
    """
    JEDI_COMMAND = 'goto_assignment'


class AnacondaGotoPythonObject(AnacondaGoto):
    """Open prompt asking for Python path and JediGoto
    """

    def input_package(__tmp0, __tmp5) :
        splitted = __tmp5.strip().split('.')
        if len(splitted) == 1:
            __tmp2 = 'import %s' % splitted[0]
        else:
            __tmp2 = 'from %s import %s' % (
                '.'.join(splitted[:-1]), splitted[-1]
            )
        __tmp0.goto_python_object(__tmp2)

    def goto_python_object(__tmp0, __tmp2) -> None:
        try:
            data = {
                'filename': '',
                'method': 'goto',
                'line': 1,
                'offset': len(__tmp2),
                'source': __tmp2,
                'handler': 'jedi'
            }
            Worker().execute(__tmp0.on_success, **data)
        except:
            raise

    def __tmp4(__tmp0, __tmp3: sublime.Edit) -> None:
        sublime.active_window().show_input_panel(
            'Provide object path:', '',
            __tmp0.input_package, None, None
        )
