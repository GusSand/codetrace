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


def __tmp0(__tmp5: str, __tmp6):
    if highlight is None:
        return __tmp5
    else:
        formatter = HtmlFormatter(noclasses=True, style='trac')
        if __tmp6 == 'html+django':
            lexer = HtmlDjangoLexer()
        elif __tmp6 == 'python':
            lexer = PythonLexer()
        else:
            raise ValueError('unknown filetype: {}'.format(__tmp6))
        return SafeString(highlight(__tmp5, lexer, formatter))


def __tmp7(__tmp4):
    '''
    Remove the leading docstring from the given source code.
    '''

    mod = ast.parse(__tmp4)
    first_non_docstring = mod.body[1]
    return '\n'.join(__tmp4.splitlines()[first_non_docstring.lineno - 1:])


def __tmp3(__tmp4: <FILL>):
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
    return __tmp0(__tmp7(f.read_text()), 'python')
