
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

"""Common jedi class to work with Jedi functions
"""

import sublime
from functools import partial

from ._typing import Union, Dict


class JediUsages(object):
    """Work with Jedi definitions
    """

    def __tmp2(__tmp0, text):
        __tmp0.text = text

    def __tmp1(__tmp0, __tmp5: bool=False, data: Dict =None) :
        """Process the definitions
        """

        view = __tmp0.text.view
        if not data['success']:
            sublime.status_message('Unable to find {}'.format(
                view.substr(view.word(view.sel()[0])))
            )
            return

        definitions = data['goto'] if not __tmp5 else data['usages']
        if len(definitions) == 0:
            sublime.status_message('Unable to find {}'.format(
                view.substr(view.word(view.sel()[0])))
            )
            return

        if definitions is not None and len(definitions) == 1 and not __tmp5:
            __tmp0._jump(*definitions[0])
        else:
            __tmp0._show_options(definitions, __tmp5)

    def _jump(__tmp0, __tmp3, lineno: int =None,
              columno: int =None, transient: bool =False) :
        """Jump to a window
        """

        # process jumps from options window
        if type(__tmp3) is int:
            if __tmp3 == -1:
                # restore view
                view = __tmp0.text.view
                point = __tmp0.point

                sublime.active_window().focus_view(view)
                view.show(point)

                if view.sel()[0] != point:
                    view.sel().clear()
                    view.sel().add(point)

                return

        opts = __tmp0.options[__tmp3]
        if len(__tmp0.options[__tmp3]) == 4:
            opts = opts[1:]

        __tmp3, lineno, columno = opts
        flags = sublime.ENCODED_POSITION
        if transient:
            flags |= sublime.TRANSIENT

        sublime.active_window().open_file(
            '{}:{}:{}'.format(__tmp3, lineno or 0, columno or 0),
            flags
        )

        __tmp0._toggle_indicator(lineno, columno)

    def _show_options(__tmp0, __tmp4, __tmp5: <FILL>) :
        """Show a dropdown quickpanel with options to jump
        """

        view = __tmp0.text.view
        if __tmp5 or (not __tmp5 and type(__tmp4) is not str):
            if len(__tmp4) == 4:
                options = [[
                    o[0], o[1], 'line: {} column: {}'.format(o[2], o[3])
                ] for o in __tmp4]
            else:
                options = [[
                    o[0], 'line: {} column: {}'.format(o[1], o[2])
                ] for o in __tmp4]
        else:
            if len(__tmp4):
                options = __tmp4[0]
            else:
                sublime.status_message('Unable to find {}'.format(
                    view.substr(view.word(view.sel()[0])))
                )
                return

        __tmp0.options = __tmp4
        __tmp0.point = __tmp0.text.view.sel()[0]
        __tmp0.text.view.window().show_quick_panel(
            options, __tmp0._jump,
            on_highlight=partial(__tmp0._jump, transient=True)
        )

    def _toggle_indicator(__tmp0, lineno: int =0, columno: int =0) :
        """Toggle mark indicator for focus the cursor
        """

        pt = __tmp0.text.view.text_point(lineno - 1, columno)
        region_name = 'anaconda.indicator.{}.{}'.format(
            __tmp0.text.view.id(), lineno
        )

        for i in range(3):
            delta = 300 * i * 2
            sublime.set_timeout(lambda: __tmp0.text.view.add_regions(
                region_name,
                [sublime.Region(pt, pt)],
                'comment',
                'bookmark',
                sublime.DRAW_EMPTY_AS_OVERWRITE
            ), delta)
            sublime.set_timeout(
                lambda: __tmp0.text.view.erase_regions(region_name),
                delta + 300
            )
