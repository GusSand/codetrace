from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def render_source(__tmp3, filetype: __typ0):
    if highlight is None:
        return __tmp3
    else:
        formatter = HtmlFormatter(noclasses=True, style='trac')
        if filetype == 'html+django':
            lexer = HtmlDjangoLexer()
        elif filetype == 'python':
            lexer = PythonLexer()
        else:
            raise ValueError('unknown filetype: {}'.format(filetype))
        return SafeString(highlight(__tmp3, lexer, formatter))


def clean_python_source(__tmp1: __typ0):
    '''
    Remove the leading docstring from the given source code.
    '''

    mod = ast.parse(__tmp1)
    first_non_docstring = mod.body[1]
    return '\n'.join(__tmp1.splitlines()[first_non_docstring.lineno - 1:])


def clean_template_source(__tmp1):
    '''
    Remove any un-indented {% include %} tags in the given template source.
    '''

    return '\n'.join(
        line for line in __tmp1.splitlines()
        if not line.startswith(r'{% include')
    )


def __tmp0(f: Path):
    return render_source(clean_template_source(f.read_text()), 'html+django')


def __tmp2(f: <FILL>):
    return render_source(clean_python_source(f.read_text()), 'python')
