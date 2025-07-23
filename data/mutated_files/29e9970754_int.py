
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import sublime
import sublime_plugin

from ..anaconda_lib.worker import Worker
from ..anaconda_lib.typing import Dict, Any
from ..anaconda_lib.callback import Callback
from ..anaconda_lib.helpers import get_settings


class AnacondaMcCabe(sublime_plugin.WindowCommand):
    """Execute McCabe complexity checker
    """

    def __tmp4(__tmp0) -> None:

        view = __tmp0.window.active_view()
        code = view.substr(sublime.Region(0, view.size()))
        __tmp1 = {
            'code': code,
            'threshold': get_settings(view, 'mccabe_threshold', 7),
            'filename': view.file_name(),
            'method': 'mccabe',
            'handler': 'qa'
        }
        Worker().execute(Callback(on_success=__tmp0.prepare_data), **__tmp1)

    def __tmp3(__tmp0) :
        """Determine if this command is enabled or not
        """

        view = __tmp0.window.active_view()
        location = view.sel()[0].begin()
        matcher = 'source.python'
        return view.match_selector(location, matcher)

    def prepare_data(__tmp0, __tmp1: Dict[str, Any]) :
        """Prepare the data to present in the quick panel
        """

        if not __tmp1['success'] or __tmp1['errors'] is None:
            sublime.status_message('Unable to run McCabe checker...')
            return

        if len(__tmp1['errors']) == 0:
            view = __tmp0.window.active_view()
            threshold = get_settings(view, 'mccabe_threshold', 7)
            sublime.status_message(
                'No code complexity beyond {} was found'.format(threshold)
            )

        __tmp0._show_options(__tmp1['errors'])

    def _show_options(__tmp0, options: Dict[str, Any]) :
        """Show a dropdown quickpanel with options to jump
        """

        __tmp0.options = []  # type: List[List[str]]
        for option in options:
            __tmp0.options.append(
                [option['message'], 'line: {}'.format(option['line'])]
            )

        __tmp0.window.show_quick_panel(__tmp0.options, __tmp0._jump)

    def _jump(__tmp0, __tmp2: <FILL>) :
        """Jump to a line in the view buffer
        """

        if __tmp2 == -1:
            return

        lineno = int(__tmp0.options[__tmp2][1].split(':')[1].strip()) - 1
        pt = __tmp0.window.active_view().text_point(lineno, 0)
        __tmp0.window.active_view().sel().clear()
        __tmp0.window.active_view().sel().add(sublime.Region(pt))

        __tmp0.window.active_view().show(pt)
