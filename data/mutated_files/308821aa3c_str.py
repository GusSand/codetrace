@dataclass
class __typ0(Visitor[T]):
    tree_depth: int = 0

    def visit_default(__tmp1, __tmp2) -> Iterator[T]:
        indent = ' ' * (2 * __tmp1.tree_depth)
        if isinstance(__tmp2, Node):
            _type = type_repr(__tmp2.type)
            out(f'{indent}{_type}', fg='yellow')
            __tmp1.tree_depth += 1
            for child in __tmp2.children:
                yield from __tmp1.visit(child)

            __tmp1.tree_depth -= 1
            out(f'{indent}/{_type}', fg='yellow', bold=False)
        else:
            _type = token.tok_name.get(__tmp2.type, str(__tmp2.type))
            out(f'{indent}{_type}', fg='blue', nl=False)
            if __tmp2.prefix:
                # We don't have to handle prefixes for `Node` objects since
                # that delegates to the first child anyway.
                out(f' {__tmp2.prefix!r}', fg='green', bold=False, nl=False)
            out(f' {__tmp2.value!r}', fg='blue', bold=False)

    @classmethod
    def show(cls, __tmp0: <FILL>) :
        """Pretty-prints a given string of `code`.

        Convenience method for debugging.
        """
        v: __typ0[None] = __typ0()
        list(v.visit(lib2to3_parse(__tmp0)))
