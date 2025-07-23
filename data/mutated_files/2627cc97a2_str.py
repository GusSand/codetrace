
# Copyright (C) 2015 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

import os
import glob
import logging
from string import Template

import sublime

from .helpers import get_settings


class Phantom(object):
    """Just a wrapper around Sublime Text 3 phantoms
    """

    themes = {}  # type: Dict[str, bytes]
    templates = {}  # type: Dict[str, str]
    loaded = False
    phantomsets = {}

    def __init__(__tmp1) :
        if int(sublime.version()) < 3124:
            return

        if Phantom.loaded is False:
            __tmp1._load_css_themes()
            __tmp1._load_phantom_templates()
            Phantom.loaded = True

    def clear_phantoms(__tmp1, __tmp2):
        if not __tmp1.loaded:
            return

        vid = __tmp2.id()
        if vid in __tmp1.phantomsets:
            __tmp1.phantomsets[vid].update([])

    def update_phantoms(__tmp1, __tmp2, phantoms):
        if not __tmp1.loaded:
            return

        thmname = get_settings(__tmp2, 'anaconda_linter_phantoms_theme', 'phantom')
        tplname = get_settings(__tmp2, 'anaconda_linter_phantoms_template', 'default')

        thm = __tmp1.themes.get(thmname, __tmp1.themes['phantom'])
        tpl = __tmp1.templates.get(tplname, __tmp1.templates['default'])

        vid = __tmp2.id()
        if vid not in __tmp1.phantomsets:
            __tmp1.phantomsets[vid] = sublime.PhantomSet(__tmp2, 'Anaconda')

        sublime_phantoms = []
        for item in phantoms:
            region = __tmp2.full_line(__tmp2.text_point(item['line'], 0))
            context = {'css': thm}
            context.update(item)
            content = tpl.safe_substitute(context)
            sublime_phantoms.append(sublime.Phantom(region, content, sublime.LAYOUT_BLOCK))

        __tmp1.phantomsets[vid].update(sublime_phantoms)

    def _load_phantom_templates(__tmp1) -> None:
        """Load phantoms templates from anaconda phantoms templates
        """

        template_files_pattern = os.path.join(
            os.path.dirname(__file__), os.pardir,
            'templates', 'phantoms', '*.tpl')
        for template_file in glob.glob(template_files_pattern):
            with open(template_file, 'r', encoding='utf8') as tplfile:
                tplname = os.path.basename(template_file).split('.tpl')[0]
                tpldata = '<style>${{css}}</style>{}'.format(tplfile.read())
                __tmp1.templates[tplname] = Template(tpldata)

    def _load_css_themes(__tmp1) -> None:
        """
        Load any css theme found in the anaconda CSS themes directory
        or in the User/Anaconda.themes directory
        """

        css_files_pattern = os.path.join(
            os.path.dirname(__file__), os.pardir, 'css', '*.css')
        for __tmp0 in glob.glob(css_files_pattern):
            logging.info('anaconda: {} css theme loaded'.format(
                __tmp1._load_css(__tmp0))
            )

        packages = sublime.active_window().extract_variables()['packages']
        user_css_path = os.path.join(packages, 'User', 'Anaconda.themes')
        if os.path.exists(user_css_path):
            css_files_pattern = os.path.join(user_css_path, '*.css')
            for __tmp0 in glob.glob(css_files_pattern):
                logging.info(
                    'anaconda: {} user css theme loaded',
                    __tmp1._load_css(__tmp0)
                )

    def _load_css(__tmp1, __tmp0: <FILL>) :
        """Load a css file
        """

        theme_name = os.path.basename(__tmp0).split('.css')[0]
        with open(__tmp0, 'r') as resource:
            __tmp1.themes[theme_name] = resource.read()

        return theme_name
