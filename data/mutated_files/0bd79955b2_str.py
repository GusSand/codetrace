import re
from pathlib import Path
from typing import Match
from django.conf import settings
from django.utils.safestring import SafeString
from django.utils.module_loading import import_string
from django.urls import reverse

from .render_source import render_template_source, render_python_source

APP_DIR = Path(__file__).resolve().parent
PY_DIR = APP_DIR / 'examples'
TEMPLATES_DIR = APP_DIR / 'templates' / 'examples'
JINJA2_DIR = APP_DIR / 'jinja2' / 'examples'


def add_links_to_docs(text: <FILL>) :
    '''
    This somewhat hacky function takes a string of documentation and
    adds Sphinx documentation hyperlinks to anything that looks like a
    reference to a uswds_forms object.

    Note that it's assumed the text passed in is trusted.
    '''

    def hyperlink(__tmp2) :
        end_text = ''
        objname = __tmp2.group(0)
        if objname.endswith('.'):
            end_text = objname[-1]
            objname = objname[:-1]
        _, short_objname = objname.split('.', 1)

        # Try importing the string, to make sure it's not pointing at
        # a symbol that doesn't actually exist.
        import_string(objname)

        return '<a href="{}reference.html#{}"><code>{}</code></a>{}'.format(
            settings.DOCS_URL,
            objname,
            short_objname,
            end_text
        )

    text = re.sub(
        r'uswds_forms\.([a-zA-Z0-9_.]+)',
        hyperlink,
        text
    )
    return text


class Example:
    def __init__(__tmp1, basename, load: bool=False) :
        __tmp1.basename = basename
        __tmp1.template_path = TEMPLATES_DIR / (basename + '.html')
        __tmp1.jinja2_path = JINJA2_DIR / (basename + '.html')
        __tmp1.python_path = PY_DIR / (basename + '.py')

        if load:
            __tmp1.load()

    def load(__tmp1):
        __tmp1.view = import_string('app.examples.' + __tmp1.basename + '.view')
        __tmp1.module = import_string('app.examples.' + __tmp1.basename)

        docstr = import_string('app.examples.' + __tmp1.basename + '.__doc__')
        __tmp1.name, description = docstr.split('\n\n', 1)
        __tmp1.description = SafeString(add_links_to_docs(description))
        __tmp1.python_source = render_python_source(__tmp1.python_path)

    @property
    def template_source(__tmp1):
        return render_template_source(__tmp1.template_path)

    @property
    def __tmp0(__tmp1):
        return render_template_source(__tmp1.jinja2_path)

    @property
    def url(__tmp1):
        return reverse('example', args=(__tmp1.basename,))

    def render(__tmp1, request):
        # This is sort of weird because we're decoding the
        # content in a HttpResponse; it's not an ideal API,
        # but we want the examples be as conventional as
        # possible so they don't confuse readers, and having
        # them return HttpResponse objects like normal Django
        # views is the easiest way to accomplish that.
        return SafeString(__tmp1.view(request).content.decode('utf-8'))
