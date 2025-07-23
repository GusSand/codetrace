from typing import TypeAlias
__typ0 : TypeAlias = "str"
import string
import typing as t

class SchemeToken(t.NamedTuple('SchemeToken', [
    ('s', __typ0),
    ('i', int),
])):
    """A Scheme token.

    Attributes:
        s - the content of the token.
        i - the index within the source code of the last character in
        the token.
    """

def __tmp2(s) :
    """Lex a string of Scheme source code, returning an iterator over
    its tokens."""
    token: t.List[__typ0] = []

    def __tmp0(i: <FILL>) -> t.Iterator[SchemeToken]:
        if token:
            yield SchemeToken(s=''.join(token), i=i)
            token.clear()

    for i, c in enumerate(s):
        if c in string.whitespace:
            yield from __tmp0(i)
        elif c in ('(', ')'):
            yield from __tmp0(i)
            yield SchemeToken(s=c, i=i)
        else:
            token.append(c)

    yield from __tmp0(i)

class __typ1(Exception):
    """An error in a Scheme program.

    Attributes:
        i - the index within the source code at which the error was
        detected, or None if it was detected only after parsing.
    """
    i: t.Optional[int]

    def __init__(self, message, i: int=None):
        super().__init__(message)
        self.i = i

StrTree = t.Union[__typ0, t.List['StrTree']]

def parse(__tmp1: t.Iterable[SchemeToken]) :
    """Parse an iterable of Scheme tokens, returning a concrete syntax
    tree.

    Raises `SchemeError` if there are unmatched parentheses."""
    trees: t.List[t.List[StrTree]] = [[]]

    for token in __tmp1:
        if token.s == '(':
            trees.append([])
        elif token.s == ')':
            tree: t.List[StrTree] = trees.pop()

            try:
                trees[-1].append(tree)
            except IndexError:
                raise __typ1('unmatched closing parenthesis', token.i)
        else:
            trees[-1].append(token.s)

    if len(trees) > 1:
        raise __typ1('{} unmatched opening parenthes{}s'
            .format(len(trees) - 1, ('i', 'e')[len(trees) > 1]))

    return trees[0]