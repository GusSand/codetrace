from typing import TypeAlias
__typ1 : TypeAlias = "str"

# Copyright (C) 2015 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import os
import glob
import logging
from string import Template

import sublime

from .helpers import get_settings
from ._typing import Callable, Union, Dict


class __typ0(object):
    """Just a wrapper around Sublime Text 3 tooltips
    """

    themes = {}  # type: Dict[str, bytes]
    tooltips = {}  # type: Dict[str, str]
    loaded = False
    basesize = 75

    def __init__(__tmp1, theme) -> None:
        __tmp1.theme = theme

        if int(sublime.version()) < 3070:
            return

        if __typ0.loaded is False:
            __tmp1._load_css_themes()
            __tmp1._load_tooltips()
            __typ0.loaded = True

    def __tmp2(__tmp1, __tmp0, __tmp4, __tmp3, __tmp5: <FILL>) :  # noqa
        """Generates and display a tooltip or pass execution to fallback
        """

        st_ver = int(sublime.version())
        if st_ver < 3070:
            return __tmp5()

        width = get_settings(__tmp0, 'font_size', 8) * 75
        kwargs = {'location': -1, 'max_width': width if width < 900 else 900}
        if st_ver >= 3071:
            kwargs['flags'] = sublime.COOPERATE_WITH_AUTO_COMPLETE
        text = __tmp1._generate(__tmp4, __tmp3)
        if text is None:
            return __tmp5()

        return __tmp0.show_popup(text, **kwargs)

    def _generate(__tmp1, __tmp4, __tmp3) :  # noqa
        """Generate a tooltip with the given text
        """

        try:
            t = __tmp1.theme
            theme = __tmp1.themes[t] if t in __tmp1.themes else __tmp1.themes['popup']  # noqa
            context = {'css': theme}
            context.update(__tmp3)
            data = __tmp1.tooltips[__tmp4].safe_substitute(context)
            return data
        except KeyError as err:
            logging.error(
                'while generating tooltip: tooltip {} don\'t exists'.format(
                    __typ1(err))
            )
            return None

    def _load_tooltips(__tmp1) :
        """Load tooltips templates from anaconda tooltips templates
        """

        template_files_pattern = os.path.join(
            os.path.dirname(__file__), os.pardir,
            'templates', 'tooltips', '*.tpl')
        for template_file in glob.glob(template_files_pattern):
            with open(template_file, 'r', encoding='utf8') as tplfile:
                tplname = os.path.basename(template_file).split('.tpl')[0]
                tpldata = '<style>${{css}}</style>{}'.format(tplfile.read())
                __tmp1.tooltips[tplname] = Template(tpldata)

    def _load_css_themes(__tmp1) :
        """
        Load any css theme found in the anaconda CSS themes directory
        or in the User/Anaconda.themes directory
        """

        css_files_pattern = os.path.join(
            os.path.dirname(__file__), os.pardir, 'css', '*.css')
        for css_file in glob.glob(css_files_pattern):
            logging.info('anaconda: {} css theme loaded'.format(
                __tmp1._load_css(css_file))
            )

        packages = sublime.active_window().extract_variables()['packages']
        user_css_path = os.path.join(packages, 'User', 'Anaconda.themes')
        if os.path.exists(user_css_path):
            css_files_pattern = os.path.join(user_css_path, '*.css')
            for css_file in glob.glob(css_files_pattern):
                logging.info(
                    'anaconda: {} user css theme loaded',
                    __tmp1._load_css(css_file)
                )

    def _load_css(__tmp1, css_file) -> __typ1:
        """Load a css file
        """

        theme_name = os.path.basename(css_file).split('.css')[0]
        with open(css_file, 'r') as resource:
            __tmp1.themes[theme_name] = resource.read()

        return theme_name
