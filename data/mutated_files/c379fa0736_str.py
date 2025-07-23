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


def __tmp0(contents: <FILL>, filetype: str):
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


def clean_python_source(__tmp4: str):
    '''
    Remove the leading docstring from the given source code.
    '''

    mod = ast.parse(__tmp4)
    first_non_docstring = mod.body[1]
    return '\n'.join(__tmp4.splitlines()[first_non_docstring.lineno - 1:])


def __tmp3(__tmp4: str):
    '''
    Remove any un-indented {% include %} tags in the given template source.
    '''

    return '\n'.join(
        line for line in __tmp4.splitlines()
        if not line.startswith(r'{% include')
    )


def __tmp2(f):
    return __tmp0(__tmp3(f.read_text()), 'html+django')


def __tmp1(f: __typ0):
    return __tmp0(clean_python_source(f.read_text()), 'python')
