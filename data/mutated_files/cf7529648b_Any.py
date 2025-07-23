
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import logging
import traceback

import sublime
import sublime_plugin

from ..anaconda_lib.worker import Worker
from ..anaconda_lib._typing import Dict, Any
from ..anaconda_lib.progress_bar import ProgressBar
from ..anaconda_lib.helpers import get_settings, is_python, get_window_view
from ..anaconda_lib.jsonclient import Callback


class __typ0(sublime_plugin.TextCommand):
    """Execute autopep8 formating
    """

    data = None

    def run(__tmp0, edit) :
        if __tmp0.data is not None:
            __tmp0.replace(edit)
            return

        aggresive_level = get_settings(__tmp0.view, 'aggressive', 0)
        if aggresive_level > 0:
            if not sublime.ok_cancel_dialog(
                'You have an aggressive level of {} this may cause '
                'anaconda to change things that you don\'t really want to '
                'change.\n\nAre you sure do you want to continue?'.format(
                    aggresive_level
                )
            ):
                return

        __tmp0.code = __tmp0.view.substr(sublime.Region(0, __tmp0.view.size()))
        settings = {
            'aggressive': aggresive_level,
            'list-fixes': get_settings(__tmp0.view, 'list-fixes', False),
            'autoformat_ignore': get_settings(
                __tmp0.view, 'autoformat_ignore', []
            ),
            'autoformat_select': get_settings(
                __tmp0.view, 'autoformat_select', []
            ),
            'pep8_max_line_length': get_settings(
                __tmp0.view, 'pep8_max_line_length', 79
            ),
            'tab_size': get_settings(__tmp0.view, 'tab_size', 4)
        }
        try:
            messages = {
                'start': 'Autoformatting please wait... ',
                'end': 'Autoformatting done!',
                'fail': 'Autoformatting failed, buffer not changed.',
                'timeout': 'Autoformatting failed, buffer not changed.',
            }
            __tmp0.pbar = ProgressBar(messages)
            __tmp0.pbar.start()
            __tmp0.view.set_read_only(True)

            data = {
                'vid': __tmp0.view.id(),
                'code': __tmp0.code,
                'method': 'pep8',
                'settings': settings,
                'handler': 'autoformat'
            }
            timeout = get_settings(__tmp0.view, 'auto_formatting_timeout', 1)

            callback = Callback(timeout=timeout)
            callback.on(success=__tmp0.get_data)
            callback.on(error=__tmp0.on_failure)
            callback.on(timeout=__tmp0.on_failure)

            Worker().execute(callback, **data)
        except:
            logging.error(traceback.format_exc())

    def on_failure(__tmp0, *args, **kwargs: <FILL>) :
        __tmp0.pbar.terminate(status=__tmp0.pbar.Status.FAILURE)
        __tmp0.view.set_read_only(False)

    def is_enabled(__tmp0) -> bool:
        """Determine if this command is enabled or not
        """

        return is_python(__tmp0.view, True)

    def get_data(__tmp0, data) :
        """Collect the returned data from autopep8
        """

        __tmp0.data = data
        __tmp0.pbar.terminate()
        __tmp0.view.set_read_only(False)
        __tmp0.view.run_command('anaconda_auto_format')

    def replace(__tmp0, edit) -> None:
        """Replace the old code with what autopep8 gave to us
        """

        view = get_window_view(__tmp0.data['vid'])
        if __tmp0.code != __tmp0.data.get('buffer'):
            region = sublime.Region(0, view.size())
            view.replace(edit, region, __tmp0.data.get('buffer'))
            if get_settings(view, 'auto_formatting'):
                sublime.set_timeout(lambda: view.run_command("save"), 0)

        __tmp0.code = None
        __tmp0.data = None
