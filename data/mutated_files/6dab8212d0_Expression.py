from typing import TypeAlias
__typ16 : TypeAlias = "TypeApplication"
__typ12 : TypeAlias = "TupleExpr"
__typ10 : TypeAlias = "MemberExpr"
__typ15 : TypeAlias = "SliceExpr"
__typ13 : TypeAlias = "LambdaExpr"
__typ1 : TypeAlias = "BackquoteExpr"
__typ19 : TypeAlias = "StarExpr"
__typ5 : TypeAlias = "OpExpr"
__typ8 : TypeAlias = "DictionaryComprehension"
__typ11 : TypeAlias = "RevealTypeExpr"
__typ22 : TypeAlias = "YieldExpr"
__typ18 : TypeAlias = "IndexExpr"
__typ9 : TypeAlias = "Node"
__typ20 : TypeAlias = "ConditionalExpr"
__typ2 : TypeAlias = "SetExpr"
__typ0 : TypeAlias = "GeneratorExpr"
__typ7 : TypeAlias = "ListExpr"
__typ6 : TypeAlias = "YieldFromExpr"
__typ3 : TypeAlias = "AwaitExpr"
__typ21 : TypeAlias = "CallExpr"
__typ4 : TypeAlias = "ComparisonExpr"
__typ17 : TypeAlias = "DictExpr"
"""Find all subexpressions of an AST node."""

from typing import List

from mypy.nodes import (
    Expression, Node, MemberExpr, YieldFromExpr, YieldExpr, CallExpr, OpExpr, ComparisonExpr,
    SliceExpr, CastExpr, RevealTypeExpr, UnaryExpr, ListExpr, TupleExpr, DictExpr, SetExpr,
    IndexExpr, GeneratorExpr, ListComprehension, SetComprehension, DictionaryComprehension,
    ConditionalExpr, TypeApplication, LambdaExpr, StarExpr, BackquoteExpr, AwaitExpr,
)
from mypy.traverser import TraverserVisitor


def get_subexpressions(node: __typ9) -> List[Expression]:
    visitor = __typ14()
    node.accept(visitor)
    return visitor.expressions


class __typ14(TraverserVisitor):
    def __tmp1(__tmp0) -> None:
        __tmp0.expressions = []  # type: List[Expression]

    def __tmp2(__tmp0, o: <FILL>) -> None:
        __tmp0.add(o)

    visit_int_expr = __tmp2
    visit_name_expr = __tmp2
    visit_float_expr = __tmp2
    visit_str_expr = __tmp2
    visit_bytes_expr = __tmp2
    visit_unicode_expr = __tmp2
    visit_complex_expr = __tmp2
    visit_ellipsis = __tmp2
    visit_super_expr = __tmp2
    visit_type_var_expr = __tmp2
    visit_type_alias_expr = __tmp2
    visit_namedtuple_expr = __tmp2
    visit_typeddict_expr = __tmp2
    visit__promote_expr = __tmp2
    visit_newtype_expr = __tmp2

    def visit_member_expr(__tmp0, e: __typ10) -> None:
        __tmp0.add(e)
        super().visit_member_expr(e)

    def visit_yield_from_expr(__tmp0, e: __typ6) -> None:
        __tmp0.add(e)
        super().visit_yield_from_expr(e)

    def visit_yield_expr(__tmp0, e: __typ22) :
        __tmp0.add(e)
        super().visit_yield_expr(e)

    def visit_call_expr(__tmp0, e: __typ21) -> None:
        __tmp0.add(e)
        super().visit_call_expr(e)

    def visit_op_expr(__tmp0, e: __typ5) -> None:
        __tmp0.add(e)
        super().visit_op_expr(e)

    def visit_comparison_expr(__tmp0, e: __typ4) -> None:
        __tmp0.add(e)
        super().visit_comparison_expr(e)

    def visit_slice_expr(__tmp0, e: __typ15) -> None:
        __tmp0.add(e)
        super().visit_slice_expr(e)

    def visit_cast_expr(__tmp0, e: CastExpr) -> None:
        __tmp0.add(e)
        super().visit_cast_expr(e)

    def visit_reveal_type_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_reveal_type_expr(e)

    def visit_unary_expr(__tmp0, e: UnaryExpr) -> None:
        __tmp0.add(e)
        super().visit_unary_expr(e)

    def visit_list_expr(__tmp0, e: __typ7) -> None:
        __tmp0.add(e)
        super().visit_list_expr(e)

    def visit_tuple_expr(__tmp0, e: __typ12) -> None:
        __tmp0.add(e)
        super().visit_tuple_expr(e)

    def visit_dict_expr(__tmp0, e: __typ17) -> None:
        __tmp0.add(e)
        super().visit_dict_expr(e)

    def visit_set_expr(__tmp0, e: __typ2) :
        __tmp0.add(e)
        super().visit_set_expr(e)

    def visit_index_expr(__tmp0, e: __typ18) -> None:
        __tmp0.add(e)
        super().visit_index_expr(e)

    def visit_generator_expr(__tmp0, e: __typ0) -> None:
        __tmp0.add(e)
        super().visit_generator_expr(e)

    def visit_dictionary_comprehension(__tmp0, e: __typ8) -> None:
        __tmp0.add(e)
        super().visit_dictionary_comprehension(e)

    def visit_list_comprehension(__tmp0, e: ListComprehension) -> None:
        __tmp0.add(e)
        super().visit_list_comprehension(e)

    def visit_set_comprehension(__tmp0, e: SetComprehension) -> None:
        __tmp0.add(e)
        super().visit_set_comprehension(e)

    def visit_conditional_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_conditional_expr(e)

    def visit_type_application(__tmp0, e: __typ16) -> None:
        __tmp0.add(e)
        super().visit_type_application(e)

    def visit_lambda_expr(__tmp0, e: __typ13) -> None:
        __tmp0.add(e)
        super().visit_lambda_expr(e)

    def visit_star_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_star_expr(e)

    def visit_backquote_expr(__tmp0, e: __typ1) -> None:
        __tmp0.add(e)
        super().visit_backquote_expr(e)

    def visit_await_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_await_expr(e)

    def add(__tmp0, e: Expression) -> None:
        __tmp0.expressions.append(e)
