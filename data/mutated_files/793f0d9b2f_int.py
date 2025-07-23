from typing import TypeAlias
__typ0 : TypeAlias = "bool"

# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import sublime
import sublime_plugin

from ..anaconda_lib.typing import Dict, Any
from ..anaconda_lib.helpers import get_settings
from ..anaconda_lib.helpers import valid_languages
from ..anaconda_lib.linting.sublime import ANACONDA


class AnacondaGetLines(sublime_plugin.WindowCommand):
    """Get a quickpanel with all the errors and lines ready to jump to them
    """

    def __tmp4(__tmp0) :
        errors = {}  # type: Dict[int, str]
        __tmp0._harvest_errors(errors, 'ERRORS')
        __tmp0._harvest_errors(errors, 'WARNINGS')
        __tmp0._harvest_errors(errors, 'VIOLATIONS')

        if len(errors) > 0:
            __tmp0.options = []  # type: List[List[str]]
            for line, error_strings in errors.items():

                for msg in error_strings:
                    __tmp0.options.append([msg, 'line: {}'.format(line)])

            __tmp0.window.show_quick_panel(__tmp0.options, __tmp0._jump)

    def __tmp2(__tmp0) -> __typ0:
        """Determines if the command is enabled
        """

        view = __tmp0.window.active_view()
        if (view.file_name() in ANACONDA['DISABLED']
                or not get_settings(view, 'anaconda_linting')):
            return False

        location = view.sel()[0].begin()
        for lang in valid_languages():
            matcher = 'source.{}'.format(lang)
            if view.match_selector(location, matcher) is True:
                return True

        return False

    def _harvest_errors(__tmp0, __tmp3, __tmp5: str) :  # noqa
        vid = __tmp0.window.active_view().id()
        for line, error_strings in ANACONDA[__tmp5].get(vid, {}).items():
            if line not in __tmp3:
                __tmp3[line] = []

            for error in error_strings:
                __tmp3[line].append(error)

    def _jump(__tmp0, __tmp1: <FILL>) :
        """Jump to a line in the view buffer
        """

        if __tmp1 == -1:
            return

        lineno = int(__tmp0.options[__tmp1][1].split(':')[1].strip())
        pt = __tmp0.window.active_view().text_point(lineno, 0)
        __tmp0.window.active_view().sel().clear()
        __tmp0.window.active_view().sel().add(sublime.Region(pt))

        __tmp0.window.active_view().show(pt)
