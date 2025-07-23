from typing import TypeAlias
__typ11 : TypeAlias = "ConditionalExpr"
__typ13 : TypeAlias = "TypeApplication"
__typ3 : TypeAlias = "ListComprehension"
__typ9 : TypeAlias = "LambdaExpr"
__typ8 : TypeAlias = "AwaitExpr"
__typ7 : TypeAlias = "SetExpr"
__typ2 : TypeAlias = "ComparisonExpr"
__typ0 : TypeAlias = "StarExpr"
__typ6 : TypeAlias = "RevealTypeExpr"
__typ12 : TypeAlias = "SliceExpr"
__typ1 : TypeAlias = "YieldExpr"
__typ4 : TypeAlias = "MemberExpr"
__typ10 : TypeAlias = "SetComprehension"
__typ5 : TypeAlias = "GeneratorExpr"
"""Find all subexpressions of an AST node."""

from typing import List

from mypy.nodes import (
    Expression, Node, MemberExpr, YieldFromExpr, YieldExpr, CallExpr, OpExpr, ComparisonExpr,
    SliceExpr, CastExpr, RevealTypeExpr, UnaryExpr, ListExpr, TupleExpr, DictExpr, SetExpr,
    IndexExpr, GeneratorExpr, ListComprehension, SetComprehension, DictionaryComprehension,
    ConditionalExpr, TypeApplication, LambdaExpr, StarExpr, BackquoteExpr, AwaitExpr,
)
from mypy.traverser import TraverserVisitor


def __tmp0(node) :
    visitor = SubexpressionFinder()
    node.accept(visitor)
    return visitor.expressions


class SubexpressionFinder(TraverserVisitor):
    def __tmp2(__tmp1) -> None:
        __tmp1.expressions = []  # type: List[Expression]

    def __tmp3(__tmp1, o) -> None:
        __tmp1.add(o)

    visit_int_expr = __tmp3
    visit_name_expr = __tmp3
    visit_float_expr = __tmp3
    visit_str_expr = __tmp3
    visit_bytes_expr = __tmp3
    visit_unicode_expr = __tmp3
    visit_complex_expr = __tmp3
    visit_ellipsis = __tmp3
    visit_super_expr = __tmp3
    visit_type_var_expr = __tmp3
    visit_type_alias_expr = __tmp3
    visit_namedtuple_expr = __tmp3
    visit_typeddict_expr = __tmp3
    visit__promote_expr = __tmp3
    visit_newtype_expr = __tmp3

    def visit_member_expr(__tmp1, e: __typ4) :
        __tmp1.add(e)
        super().visit_member_expr(e)

    def visit_yield_from_expr(__tmp1, e) -> None:
        __tmp1.add(e)
        super().visit_yield_from_expr(e)

    def visit_yield_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_yield_expr(e)

    def visit_call_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_call_expr(e)

    def visit_op_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_op_expr(e)

    def visit_comparison_expr(__tmp1, e) -> None:
        __tmp1.add(e)
        super().visit_comparison_expr(e)

    def visit_slice_expr(__tmp1, e: __typ12) -> None:
        __tmp1.add(e)
        super().visit_slice_expr(e)

    def visit_cast_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_cast_expr(e)

    def visit_reveal_type_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_reveal_type_expr(e)

    def visit_unary_expr(__tmp1, e: UnaryExpr) :
        __tmp1.add(e)
        super().visit_unary_expr(e)

    def visit_list_expr(__tmp1, e) -> None:
        __tmp1.add(e)
        super().visit_list_expr(e)

    def visit_tuple_expr(__tmp1, e: TupleExpr) :
        __tmp1.add(e)
        super().visit_tuple_expr(e)

    def visit_dict_expr(__tmp1, e: DictExpr) -> None:
        __tmp1.add(e)
        super().visit_dict_expr(e)

    def visit_set_expr(__tmp1, e: __typ7) :
        __tmp1.add(e)
        super().visit_set_expr(e)

    def visit_index_expr(__tmp1, e: IndexExpr) -> None:
        __tmp1.add(e)
        super().visit_index_expr(e)

    def visit_generator_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_generator_expr(e)

    def visit_dictionary_comprehension(__tmp1, e: DictionaryComprehension) -> None:
        __tmp1.add(e)
        super().visit_dictionary_comprehension(e)

    def visit_list_comprehension(__tmp1, e: __typ3) :
        __tmp1.add(e)
        super().visit_list_comprehension(e)

    def visit_set_comprehension(__tmp1, e) :
        __tmp1.add(e)
        super().visit_set_comprehension(e)

    def visit_conditional_expr(__tmp1, e: __typ11) :
        __tmp1.add(e)
        super().visit_conditional_expr(e)

    def visit_type_application(__tmp1, e: __typ13) :
        __tmp1.add(e)
        super().visit_type_application(e)

    def visit_lambda_expr(__tmp1, e: __typ9) -> None:
        __tmp1.add(e)
        super().visit_lambda_expr(e)

    def visit_star_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_star_expr(e)

    def visit_backquote_expr(__tmp1, e: BackquoteExpr) :
        __tmp1.add(e)
        super().visit_backquote_expr(e)

    def visit_await_expr(__tmp1, e) :
        __tmp1.add(e)
        super().visit_await_expr(e)

    def add(__tmp1, e: <FILL>) -> None:
        __tmp1.expressions.append(e)
