from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ0 : TypeAlias = "int"

# Copyright (C) 2013 ~ 2016 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import sublime

from ._typing import List
from Default.history_list import get_jump_history_for_view


class __typ1:
    """
    Creates a panel that can be used to explore nested options sets

    The data structure for the options is as follows:

        Options[
            {
                'title': 'Title Data'
                'details': 'Details Data',
                'location': 'File: {} Line: {} Column: {}',
                'position': 'filepath:line:col',
                'options': [
                    {
                        'title': 'Title Data'
                        'details': 'Details Data',
                        'location': 'File: {} Line: {} Column: {}',
                        'position': 'filepath:line:col',
                        'options': [
                        ]...
                    }
                ]
            }
        ]

    So we can nest as many levels as we want
    """

    def __init__(__tmp0, view: sublime.View, options: List) -> None:
        __tmp0.options = options
        __tmp0.view = view
        __tmp0.selected = []  # type: List
        __tmp0.restore_point = view.sel()[0]

    def show(__tmp0, cluster: <FILL>, forced: bool=False) -> None:
        """Show the quick panel with the given options
        """

        if not cluster:
            cluster = __tmp0.options

        if len(cluster) == 1 and not forced:
            try:
                __typ3(__tmp0.view, cluster[0]['position']).jump()
            except KeyError:
                if len(cluster[0].get('options', [])) == 1 and not forced:
                    __typ3(
                        __tmp0.view, cluster[0]['options'][0]['position']).jump()
            return

        __tmp0.last_cluster = cluster
        quick_panel_options = []
        for data in cluster:
            tmp = [data['title']]
            if 'details' in data:
                tmp.append(data['details'])
            if 'location' in data:
                tmp.append(data['location'])
            quick_panel_options.append(tmp)

        __tmp0.view.window().show_quick_panel(
            quick_panel_options,
            on_select=__tmp0.on_select,
            on_highlight=lambda index: __tmp0.on_select(index, True)
        )

    def on_select(__tmp0, index, transient: bool=False) -> None:
        """Called when an option is been made in the quick panel
        """

        if index == -1:
            __tmp0._restore_view()
            return

        cluster = __tmp0.last_cluster
        node = cluster[index]
        if transient and 'options' in node:
            return

        if 'options' in node:
            __tmp0.prev_cluster = __tmp0.last_cluster
            opts = node['options'][:]
            opts.insert(0, {'title': '<- Go Back', 'position': 'back'})
            sublime.set_timeout(lambda: __tmp0.show(opts), 0)
        else:
            if node['position'] == 'back' and not transient:
                sublime.set_timeout(lambda: __tmp0.show(__tmp0.prev_cluster), 0)
            elif node['position'] != 'back':
                __typ3(__tmp0.view, node['position']).jump(transient)

    def _restore_view(__tmp0):
        """Restore the view and location
        """

        sublime.active_window().focus_view(__tmp0.view)
        __tmp0.view.show(__tmp0.restore_point)

        if __tmp0.view.sel()[0] != __tmp0.restore_point:
            __tmp0.view.sel().clear()
            __tmp0.view.sel().add(__tmp0.restore_point)


class __typ3:
    """Jump to the specified file line and column making an indicator to toggle
    """

    def __init__(__tmp0, view: sublime.View, position: __typ2) -> None:
        __tmp0.position = position
        __tmp0.view = view

    def jump(__tmp0, transient: bool=False) -> None:
        """Jump to the selection
        """

        flags = sublime.ENCODED_POSITION
        if transient is True:
            flags |= sublime.TRANSIENT

        get_jump_history_for_view(__tmp0.view).push_selection(__tmp0.view)
        sublime.active_window().open_file(__tmp0.position, flags)
        if not transient:
            __tmp0._toggle_indicator()

    def _toggle_indicator(__tmp0) -> None:
        """Toggle mark indicator to focus the cursor
        """

        path, line, column = __tmp0.position.rsplit(':', 2)
        pt = __tmp0.view.text_point(__typ0(line) - 1, __typ0(column))
        region_name = 'anaconda.indicator.{}.{}'.format(
            __tmp0.view.id(), line
        )

        for i in range(3):
            delta = 300 * i * 2
            sublime.set_timeout(lambda: __tmp0.view.add_regions(
                region_name,
                [sublime.Region(pt, pt)],
                'comment',
                'bookmark',
                sublime.DRAW_EMPTY_AS_OVERWRITE
            ), delta)
            sublime.set_timeout(
                lambda: __tmp0.view.erase_regions(region_name),
                delta + 300
            )
