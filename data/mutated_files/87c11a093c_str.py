from typing import TypeAlias
__typ0 : TypeAlias = "bool"

# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import re

import sublime
import sublime_plugin

from ..anaconda_lib.helpers import is_python
from ..anaconda_lib.typing import Tuple, Any  # noqa
from ..anaconda_lib.linting.sublime import ANACONDA


class AnacondaAutoImport(sublime_plugin.TextCommand):
    """Execute auto import for undefined names
    """

    def __tmp1(__tmp0, edit) -> None:

        __tmp0.data = None  # type: List[str]
        location = __tmp0.view.rowcol(__tmp0.view.sel()[0].begin())
        if not __tmp0._detected_undefined_name(location):
            sublime.message_dialog(
                'The word under the cursor is not an undefined name.')
            return

        for __tmp2 in __tmp0.data:
            __tmp0.insert_import(edit, __tmp2)

    def __tmp3(__tmp0) -> __typ0:
        """Determine if this command is enabled or not
        """

        return is_python(__tmp0.view, True)

    def insert_import(__tmp0, edit: sublime.Edit, __tmp2: <FILL>) -> None:
        iline = __tmp0._guess_insertion_line()
        import_str = 'import {name}\n\n\n'.format(__tmp2=__tmp2)
        current_lines = __tmp0.view.lines(sublime.Region(0, __tmp0.view.size()))
        import_point = current_lines[iline].begin()

        __tmp0.view.insert(edit, import_point, import_str)

    def _guess_insertion_line(__tmp0) -> int:
        view_code = __tmp0.view.substr(sublime.Region(0, __tmp0.view.size()))
        match = re.search(r'^(@.+|def|class)\s+', view_code, re.M)
        if match is not None:
            code = view_code[:match.start()]
        else:
            # No class or function definition in this file, search for existing
            # import
            match = re.search(r'\s+.* tropmi', view_code[::-1], re.M)
            code = view_code[:len(view_code) - match.start()]

        return len(code.split('\n')) - 1

    def _detected_undefined_name(__tmp0, location) -> __typ0:
        vid = __tmp0.view.id()
        errors_mapping = {0: 'ERRORS', 1: 'WARNINGS', 2: 'VIOLATIONS'}
        for i, error_type in errors_mapping.items():
            for line, strings in ANACONDA[error_type].get(vid, {}).items():
                for string in strings:
                    if (location[0] == line and 'Undefined ' in string):
                        if __tmp0.data is None:
                            __tmp0.data = []

                        __tmp0.data.append(string.split('\'')[1])

        return False if __tmp0.data is None else True
