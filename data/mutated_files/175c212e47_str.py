
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import logging
from functools import partial

import sublime
import sublime_plugin

from ..anaconda_lib.worker import Worker
from ..anaconda_lib.tooltips import Tooltip
from ..anaconda_lib.kite import Integration
from ..anaconda_lib._typing import Dict, Tuple, Any
from ..anaconda_lib.helpers import prepare_send_data, is_python, get_settings


class AnacondaSignaturesEventListener(sublime_plugin.EventListener):
    """Signatures on status bar event listener class
    """

    doc = None  # type: str
    signature = None
    exclude = (
        'None', 'NoneType', 'str', 'int', 'float', 'True',
        'False', 'in', 'or', 'and', 'bool'
    )

    def __tmp2(__tmp1, __tmp0) :
        """Called after changes has been made to a view
        """

        if __tmp0.command_history(0)[0] in ("expand_tabs", "unexpand_tabs"):
            return

        if not is_python(__tmp0) or not get_settings(__tmp0, 'display_signatures'):
            return

        if Integration.enabled():
            return

        try:
            location = __tmp0.rowcol(__tmp0.sel()[0].begin())
            if __tmp0.substr(__tmp0.sel()[0].begin()) in ['(', ')']:
                location = (location[0], location[1] - 1)

            data = prepare_send_data(location, 'doc', 'jedi')
            use_tooltips = get_settings(
                __tmp0, 'enable_signatures_tooltip', True
            )
            st_version = int(sublime.version())
            if st_version >= 3070:
                data['html'] = use_tooltips

            currying = partial(__tmp1.prepare_data_status, __tmp0)
            if use_tooltips and st_version >= 3070:
                currying = partial(__tmp1.prepare_data_tooltip, __tmp0)
            Worker().execute(currying, **data)
        except Exception as error:
            logging.error(error)

    def prepare_data_tooltip(
            __tmp1, __tmp0, data) :
        """Prepare the returned data for tooltips
        """

        merge_doc = get_settings(__tmp0, 'merge_signatures_and_doc')
        if (data['success'] and 'No docstring' not
                in data['doc'] and data['doc'] != 'list\n'):
            try:
                i = data['doc'].split('<br>').index("")
            except ValueError:
                __tmp1.signature = data['doc']
                __tmp1.doc = ''
                if __tmp1._signature_excluded(__tmp1.signature):
                    return
                return __tmp1._show_popup(__tmp0)

            if merge_doc:
                __tmp1.doc = '<br>'.join(data['doc'].split('<br>')[i:]).replace(
                    "  ", "&nbsp;&nbsp;")

            __tmp1.signature = '<br>&nbsp;&nbsp;&nbsp;&nbsp;'.join(
                data['doc'].split('<br>')[0:i])
            if __tmp1.signature is not None and __tmp1.signature != "":
                if not __tmp1._signature_excluded(__tmp1.signature):
                    return __tmp1._show_popup(__tmp0)

        if __tmp0.is_popup_visible():
                __tmp0.hide_popup()
        __tmp0.erase_status('anaconda_doc')

    def prepare_data_status(
            __tmp1, __tmp0, data) -> Any:
        """Prepare the returned data for status
        """

        if (data['success'] and 'No docstring' not
                in data['doc'] and data['doc'] != 'list\n'):
            __tmp1.signature = data['doc']
            if __tmp1._signature_excluded(__tmp1.signature):
                return
            try:
                __tmp1.signature = __tmp1.signature.splitlines()[2]
            except KeyError:
                return

            return __tmp1._show_status(__tmp0)

    def _show_popup(__tmp1, __tmp0) -> None:
        """Show message in a popup if sublime text version is >= 3070
        """

        show_doc = get_settings(__tmp0, 'merge_signatures_and_doc', True)
        content = {'content': __tmp1.signature}
        display_tooltip = 'signature'
        if show_doc:
            content = {'signature': __tmp1.signature, 'doc': __tmp1.doc}
            display_tooltip = 'signature_doc'

        css = get_settings(__tmp0, 'anaconda_tooltip_theme', 'popup')
        Tooltip(css).show_tooltip(
            __tmp0, display_tooltip, content, partial(__tmp1._show_status, __tmp0))

    def _show_status(__tmp1, __tmp0) :
        """Show message in the view status bar
        """

        __tmp0.set_status(
            'anaconda_doc', 'Anaconda: {}'.format(__tmp1.signature)
        )

    def _signature_excluded(__tmp1, signature: <FILL>) -> Tuple[str]:
        """Whether to supress displaying information for the given signature.
        """

        # Check for the empty string first so the indexing in the next tests
        # can't hit an exception, and we don't want to show an empty signature.
        return ((signature == "") or
                (signature.split('(', 1)[0].strip() in __tmp1.exclude) or
                (signature.lstrip().split(None, 1)[0] in __tmp1.exclude))
