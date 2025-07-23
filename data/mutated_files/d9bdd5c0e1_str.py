import string
import typing as t

class __typ1(t.NamedTuple('SchemeToken', [
    ('s', str),
    ('i', int),
])):
    """A Scheme token.

    Attributes:
        s - the content of the token.
        i - the index within the source code of the last character in
        the token.
    """

def lex(s: <FILL>) :
    """Lex a string of Scheme source code, returning an iterator over
    its tokens."""
    token: t.List[str] = []

    def flush(i) -> t.Iterator[__typ1]:
        if token:
            yield __typ1(s=''.join(token), i=i)
            token.clear()

    for i, c in enumerate(s):
        if c in string.whitespace:
            yield from flush(i)
        elif c in ('(', ')'):
            yield from flush(i)
            yield __typ1(s=c, i=i)
        else:
            token.append(c)

    yield from flush(i)

class __typ0(Exception):
    """An error in a Scheme program.

    Attributes:
        i - the index within the source code at which the error was
        detected, or None if it was detected only after parsing.
    """
    i: t.Optional[int]

    def __init__(__tmp0, message, i: int=None):
        super().__init__(message)
        __tmp0.i = i

StrTree = t.Union[str, t.List['StrTree']]

def parse(tokens: t.Iterable[__typ1]) :
    """Parse an iterable of Scheme tokens, returning a concrete syntax
    tree.

    Raises `SchemeError` if there are unmatched parentheses."""
    trees: t.List[t.List[StrTree]] = [[]]

    for token in tokens:
        if token.s == '(':
            trees.append([])
        elif token.s == ')':
            tree: t.List[StrTree] = trees.pop()

            try:
                trees[-1].append(tree)
            except IndexError:
                raise __typ0('unmatched closing parenthesis', token.i)
        else:
            trees[-1].append(token.s)

    if len(trees) > 1:
        raise __typ0('{} unmatched opening parenthes{}s'
            .format(len(trees) - 1, ('i', 'e')[len(trees) > 1]))

    return trees[0]