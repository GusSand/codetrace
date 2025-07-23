"""Translate an Expression to a Type value."""

from mypy.nodes import (
    Expression, NameExpr, MemberExpr, IndexExpr, TupleExpr,
    ListExpr, StrExpr, BytesExpr, UnicodeExpr, EllipsisExpr, CallExpr,
    ARG_POS, ARG_NAMED, get_member_expr_fullname
)
from mypy.fastparse import parse_type_comment
from mypy.types import (
    Type, UnboundType, TypeList, EllipsisType, AnyType, Optional, CallableArgument, TypeOfAny
)


class __typ0(Exception):
    """Exception raised when an expression is not valid as a type."""


def __tmp0(expr: <FILL>) :
    if isinstance(expr, NameExpr) and expr.name == 'None':
        return None
    elif isinstance(expr, StrExpr):
        return expr.value
    elif isinstance(expr, UnicodeExpr):
        return expr.value
    else:
        raise __typ0()


def __tmp1(expr, _parent: Optional[Expression] = None) :
    """Translate an expression to the corresponding type.

    The result is not semantically analyzed. It can be UnboundType or TypeList.
    Raise TypeTranslationError if the expression cannot represent a type.
    """
    # The `parent` paremeter is used in recursive calls to provide context for
    # understanding whether an CallableArgument is ok.
    name = None  # type: Optional[str]
    if isinstance(expr, NameExpr):
        name = expr.name
        return UnboundType(name, line=expr.line, column=expr.column)
    elif isinstance(expr, MemberExpr):
        fullname = get_member_expr_fullname(expr)
        if fullname:
            return UnboundType(fullname, line=expr.line, column=expr.column)
        else:
            raise __typ0()
    elif isinstance(expr, IndexExpr):
        base = __tmp1(expr.base, expr)
        if isinstance(base, UnboundType):
            if base.args:
                raise __typ0()
            if isinstance(expr.index, TupleExpr):
                args = expr.index.items
            else:
                args = [expr.index]
            base.args = [__tmp1(arg, expr) for arg in args]
            if not base.args:
                base.empty_tuple_index = True
            return base
        else:
            raise __typ0()
    elif isinstance(expr, CallExpr) and isinstance(_parent, ListExpr):
        c = expr.callee
        names = []
        # Go through the dotted member expr chain to get the full arg
        # constructor name to look up
        while True:
            if isinstance(c, NameExpr):
                names.append(c.name)
                break
            elif isinstance(c, MemberExpr):
                names.append(c.name)
                c = c.expr
            else:
                raise __typ0()
        arg_const = '.'.join(reversed(names))

        # Go through the constructor args to get its name and type.
        name = None
        default_type = AnyType(TypeOfAny.unannotated)
        typ = default_type  # type: Type
        for i, arg in enumerate(expr.args):
            if expr.arg_names[i] is not None:
                if expr.arg_names[i] == "name":
                    if name is not None:
                        # Two names
                        raise __typ0()
                    name = __tmp0(arg)
                    continue
                elif expr.arg_names[i] == "type":
                    if typ is not default_type:
                        # Two types
                        raise __typ0()
                    typ = __tmp1(arg, expr)
                    continue
                else:
                    raise __typ0()
            elif i == 0:
                typ = __tmp1(arg, expr)
            elif i == 1:
                name = __tmp0(arg)
            else:
                raise __typ0()
        return CallableArgument(typ, name, arg_const, expr.line, expr.column)
    elif isinstance(expr, ListExpr):
        return TypeList([__tmp1(t, expr) for t in expr.items],
                        line=expr.line, column=expr.column)
    elif isinstance(expr, (StrExpr, BytesExpr, UnicodeExpr)):
        # Parse string literal type.
        try:
            result = parse_type_comment(expr.value, expr.line, None)
            assert result is not None
        except SyntaxError:
            raise __typ0()
        return result
    elif isinstance(expr, EllipsisExpr):
        return EllipsisType(expr.line)
    else:
        raise __typ0()
