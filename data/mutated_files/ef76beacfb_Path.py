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


def render_source(contents: __typ0, filetype: __typ0):
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


def __tmp1(__tmp0):
    '''
    Remove the leading docstring from the given source code.
    '''

    mod = ast.parse(__tmp0)
    first_non_docstring = mod.body[1]
    return '\n'.join(__tmp0.splitlines()[first_non_docstring.lineno - 1:])


def clean_template_source(__tmp0: __typ0):
    '''
    Remove any un-indented {% include %} tags in the given template source.
    '''

    return '\n'.join(
        line for line in __tmp0.splitlines()
        if not line.startswith(r'{% include')
    )


def render_template_source(f: <FILL>):
    return render_source(clean_template_source(f.read_text()), 'html+django')


def render_python_source(f: Path):
    return render_source(__tmp1(f.read_text()), 'python')
