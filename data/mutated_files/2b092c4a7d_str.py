from typing import TypeAlias
__typ0 : TypeAlias = "int"

# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import re

import sublime
import sublime_plugin

from ..anaconda_lib.helpers import is_python
from ..anaconda_lib._typing import Tuple, Any  # noqa
from ..anaconda_lib.linting.sublime import ANACONDA


class AnacondaAutoImport(sublime_plugin.TextCommand):
    """Execute auto import for undefined names
    """

    def run(__tmp1, __tmp2: sublime.Edit) -> None:

        __tmp1.data = None  # type: List[str]
        __tmp0 = __tmp1.view.rowcol(__tmp1.view.sel()[0].begin())
        if not __tmp1._detected_undefined_name(__tmp0):
            sublime.message_dialog(
                'The word under the cursor is not an undefined name.')
            return

        for name in __tmp1.data:
            __tmp1.insert_import(__tmp2, name)

    def is_enabled(__tmp1) -> bool:
        """Determine if this command is enabled or not
        """

        return is_python(__tmp1.view, True)

    def insert_import(__tmp1, __tmp2: sublime.Edit, name: <FILL>) :
        iline = __tmp1._guess_insertion_line()
        import_str = 'import {name}\n\n\n'.format(name=name)
        current_lines = __tmp1.view.lines(sublime.Region(0, __tmp1.view.size()))
        import_point = current_lines[iline].begin()

        __tmp1.view.insert(__tmp2, import_point, import_str)

    def _guess_insertion_line(__tmp1) -> __typ0:
        view_code = __tmp1.view.substr(sublime.Region(0, __tmp1.view.size()))
        match = re.search(r'^(@.+|def|class)\s+', view_code, re.M)
        if match is not None:
            code = view_code[:match.start()]
        else:
            # No class or function definition in this file, search for existing
            # import
            match = re.search(r'\s+.* tropmi', view_code[::-1], re.M)
            code = view_code[:len(view_code) - match.start()]

        return len(code.split('\n')) - 1

    def _detected_undefined_name(__tmp1, __tmp0: Tuple[__typ0]) -> bool:
        vid = __tmp1.view.id()
        errors_mapping = {0: 'ERRORS', 1: 'WARNINGS', 2: 'VIOLATIONS'}
        for i, error_type in errors_mapping.items():
            for line, strings in ANACONDA[error_type].get(vid, {}).items():
                for string in strings:
                    if (__tmp0[0] == line and 'Undefined ' in string):
                        if __tmp1.data is None:
                            __tmp1.data = []

                        __tmp1.data.append(string.split('\'')[1])

        return False if __tmp1.data is None else True
