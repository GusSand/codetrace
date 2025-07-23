
# Copyright (C) 2015 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import os
import glob
import logging
from string import Template

import sublime

from .helpers import get_settings
from ._typing import Callable, Union, Dict


class Tooltip(object):
    """Just a wrapper around Sublime Text 3 tooltips
    """

    themes = {}  # type: Dict[str, bytes]
    tooltips = {}  # type: Dict[str, str]
    loaded = False
    basesize = 75

    def __init__(__tmp0, theme: str) :
        __tmp0.theme = theme

        if int(sublime.version()) < 3070:
            return

        if Tooltip.loaded is False:
            __tmp0._load_css_themes()
            __tmp0._load_tooltips()
            Tooltip.loaded = True

    def show_tooltip(__tmp0, view, __tmp3: <FILL>, __tmp2, __tmp4) :  # noqa
        """Generates and display a tooltip or pass execution to fallback
        """

        st_ver = int(sublime.version())
        if st_ver < 3070:
            return __tmp4()

        width = get_settings(view, 'font_size', 8) * 75
        kwargs = {'location': -1, 'max_width': width if width < 900 else 900}
        if st_ver >= 3071:
            kwargs['flags'] = sublime.COOPERATE_WITH_AUTO_COMPLETE
        text = __tmp0._generate(__tmp3, __tmp2)
        if text is None:
            return __tmp4()

        return view.show_popup(text, **kwargs)

    def _generate(__tmp0, __tmp3, __tmp2) :  # noqa
        """Generate a tooltip with the given text
        """

        try:
            t = __tmp0.theme
            theme = __tmp0.themes[t] if t in __tmp0.themes else __tmp0.themes['popup']  # noqa
            context = {'css': theme}
            context.update(__tmp2)
            data = __tmp0.tooltips[__tmp3].safe_substitute(context)
            return data
        except KeyError as err:
            logging.error(
                'while generating tooltip: tooltip {} don\'t exists'.format(
                    str(err))
            )
            return None

    def _load_tooltips(__tmp0) :
        """Load tooltips templates from anaconda tooltips templates
        """

        template_files_pattern = os.path.join(
            os.path.dirname(__file__), os.pardir,
            'templates', 'tooltips', '*.tpl')
        for template_file in glob.glob(template_files_pattern):
            with open(template_file, 'r', encoding='utf8') as tplfile:
                tplname = os.path.basename(template_file).split('.tpl')[0]
                tpldata = '<style>${{css}}</style>{}'.format(tplfile.read())
                __tmp0.tooltips[tplname] = Template(tpldata)

    def _load_css_themes(__tmp0) :
        """
        Load any css theme found in the anaconda CSS themes directory
        or in the User/Anaconda.themes directory
        """

        css_files_pattern = os.path.join(
            os.path.dirname(__file__), os.pardir, 'css', '*.css')
        for __tmp1 in glob.glob(css_files_pattern):
            logging.info('anaconda: {} css theme loaded'.format(
                __tmp0._load_css(__tmp1))
            )

        packages = sublime.active_window().extract_variables()['packages']
        user_css_path = os.path.join(packages, 'User', 'Anaconda.themes')
        if os.path.exists(user_css_path):
            css_files_pattern = os.path.join(user_css_path, '*.css')
            for __tmp1 in glob.glob(css_files_pattern):
                logging.info(
                    'anaconda: {} user css theme loaded',
                    __tmp0._load_css(__tmp1)
                )

    def _load_css(__tmp0, __tmp1) -> str:
        """Load a css file
        """

        theme_name = os.path.basename(__tmp1).split('.css')[0]
        with open(__tmp1, 'r') as resource:
            __tmp0.themes[theme_name] = resource.read()

        return theme_name
