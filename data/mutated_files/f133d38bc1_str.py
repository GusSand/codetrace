from typing import TypeAlias
__typ0 : TypeAlias = "Path"
import ast
from pathlib import Path
from django.utils.safestring import SafeString

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.lexers.templates import HtmlDjangoLexer
    from pygments.formatters import HtmlFormatter
except ImportError:
    highlight = None


def __tmp1(contents: str, filetype: <FILL>):
    if highlight is None:
        return contents
    else:
        formatter = HtmlFormatter(noclasses=True, style='trac')
        if filetype == 'html+django':
            lexer = HtmlDjangoLexer()
        elif filetype == 'python':
            lexer = PythonLexer()
        else:
            raise ValueError('unknown filetype: {}'.format(filetype))
        return SafeString(highlight(contents, lexer, formatter))


def clean_python_source(__tmp0: str):
    '''
    Remove the leading docstring from the given source code.
    '''

    mod = ast.parse(__tmp0)
    first_non_docstring = mod.body[1]
    return '\n'.join(__tmp0.splitlines()[first_non_docstring.lineno - 1:])


def clean_template_source(__tmp0):
    '''
    Remove any un-indented {% include %} tags in the given template source.
    '''

    return '\n'.join(
        line for line in __tmp0.splitlines()
        if not line.startswith(r'{% include')
    )


def render_template_source(f):
    return __tmp1(clean_template_source(f.read_text()), 'html+django')


def __tmp2(f: __typ0):
    return __tmp1(clean_python_source(f.read_text()), 'python')
