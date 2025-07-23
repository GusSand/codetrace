from typing import TypeAlias
__typ1 : TypeAlias = "str"
@dataclass
class __typ0(Visitor[T]):
    tree_depth: int = 0

    def visit_default(self, __tmp0: <FILL>) -> Iterator[T]:
        indent = ' ' * (2 * self.tree_depth)
        if isinstance(__tmp0, Node):
            _type = type_repr(__tmp0.type)
            out(f'{indent}{_type}', fg='yellow')
            self.tree_depth += 1
            for child in __tmp0.children:
                yield from self.visit(child)

            self.tree_depth -= 1
            out(f'{indent}/{_type}', fg='yellow', bold=False)
        else:
            _type = token.tok_name.get(__tmp0.type, __typ1(__tmp0.type))
            out(f'{indent}{_type}', fg='blue', nl=False)
            if __tmp0.prefix:
                # We don't have to handle prefixes for `Node` objects since
                # that delegates to the first child anyway.
                out(f' {__tmp0.prefix!r}', fg='green', bold=False, nl=False)
            out(f' {__tmp0.value!r}', fg='blue', bold=False)

    @classmethod
    def show(cls, code: __typ1) -> None:
        """Pretty-prints a given string of `code`.

        Convenience method for debugging.
        """
        v: __typ0[None] = __typ0()
        list(v.visit(lib2to3_parse(code)))
