from typing import TypeAlias
__typ1 : TypeAlias = "bool"
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import time
import logging
import traceback

import sublime
import sublime_plugin

from ..anaconda_lib.worker import Worker
from ..anaconda_lib.typing import Dict, Any
from ..anaconda_lib.callback import Callback
from ..anaconda_lib.helpers import prepare_send_data, is_python


class __typ0(sublime_plugin.TextCommand):
    """Rename the word under the cursor to the given one in its total scope
    """

    data = None  # type: Dict[str, Any]

    def __tmp4(__tmp0, __tmp2: sublime.Edit) -> None:
        if __tmp0.data is None:
            try:
                location = __tmp0.view.word(__tmp0.view.sel()[0].begin())
                old_name = __tmp0.view.substr(location)
                sublime.active_window().show_input_panel(
                    "Replace with:", old_name, __tmp0.input_replacement,
                    None, None
                )
            except:
                logging.error(traceback.format_exc())
        else:
            __tmp0.rename(__tmp2)

    def __tmp3(__tmp0) -> __typ1:
        """Determine if this command is enabled or not
        """

        return is_python(__tmp0.view)

    def input_replacement(__tmp0, __tmp1: <FILL>) -> None:
        location = __tmp0.view.rowcol(__tmp0.view.sel()[0].begin())
        data = prepare_send_data(location, 'rename', 'jedi')
        data['directories'] = sublime.active_window().folders()
        data['new_word'] = __tmp1
        Worker().execute(Callback(on_success=__tmp0.store_data), **data)

    def store_data(__tmp0, data) -> None:
        """Just store the data an call the command again
        """

        __tmp0.data = data
        __tmp0.view.run_command('anaconda_rename')

    def rename(__tmp0, __tmp2: sublime.Edit) -> None:
        """Rename in the buffer
        """

        data = __tmp0.data
        if data['success'] is True:
            for filename, data in data['renames'].items():
                for line in data:
                    view = sublime.active_window().open_file(
                        '{}:{}:0'.format(filename, line['lineno']),
                        sublime.ENCODED_POSITION
                    )
                    while view.is_loading():
                        time.sleep(0.01)

                    lines = view.lines(sublime.Region(0, view.size()))
                    view.replace(__tmp2, lines[line['lineno']], line['line'])

        __tmp0.data = None
