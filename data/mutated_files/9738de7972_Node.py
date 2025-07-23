from typing import TypeAlias
__typ2 : TypeAlias = "ListComprehension"
__typ0 : TypeAlias = "ComparisonExpr"
__typ1 : TypeAlias = "Expression"
"""Find all subexpressions of an AST node."""

from typing import List

from mypy.nodes import (
    Expression, Node, MemberExpr, YieldFromExpr, YieldExpr, CallExpr, OpExpr, ComparisonExpr,
    SliceExpr, CastExpr, RevealTypeExpr, UnaryExpr, ListExpr, TupleExpr, DictExpr, SetExpr,
    IndexExpr, GeneratorExpr, ListComprehension, SetComprehension, DictionaryComprehension,
    ConditionalExpr, TypeApplication, LambdaExpr, StarExpr, BackquoteExpr, AwaitExpr,
)
from mypy.traverser import TraverserVisitor


def get_subexpressions(node: <FILL>) -> List[__typ1]:
    visitor = SubexpressionFinder()
    node.accept(visitor)
    return visitor.expressions


class SubexpressionFinder(TraverserVisitor):
    def __init__(__tmp0) :
        __tmp0.expressions = []  # type: List[Expression]

    def _visit_leaf(__tmp0, o: __typ1) :
        __tmp0.add(o)

    visit_int_expr = _visit_leaf
    visit_name_expr = _visit_leaf
    visit_float_expr = _visit_leaf
    visit_str_expr = _visit_leaf
    visit_bytes_expr = _visit_leaf
    visit_unicode_expr = _visit_leaf
    visit_complex_expr = _visit_leaf
    visit_ellipsis = _visit_leaf
    visit_super_expr = _visit_leaf
    visit_type_var_expr = _visit_leaf
    visit_type_alias_expr = _visit_leaf
    visit_namedtuple_expr = _visit_leaf
    visit_typeddict_expr = _visit_leaf
    visit__promote_expr = _visit_leaf
    visit_newtype_expr = _visit_leaf

    def visit_member_expr(__tmp0, e) :
        __tmp0.add(e)
        super().visit_member_expr(e)

    def visit_yield_from_expr(__tmp0, e: YieldFromExpr) -> None:
        __tmp0.add(e)
        super().visit_yield_from_expr(e)

    def visit_yield_expr(__tmp0, e) :
        __tmp0.add(e)
        super().visit_yield_expr(e)

    def visit_call_expr(__tmp0, e: CallExpr) :
        __tmp0.add(e)
        super().visit_call_expr(e)

    def visit_op_expr(__tmp0, e: OpExpr) -> None:
        __tmp0.add(e)
        super().visit_op_expr(e)

    def visit_comparison_expr(__tmp0, e: __typ0) -> None:
        __tmp0.add(e)
        super().visit_comparison_expr(e)

    def visit_slice_expr(__tmp0, e: SliceExpr) -> None:
        __tmp0.add(e)
        super().visit_slice_expr(e)

    def visit_cast_expr(__tmp0, e: CastExpr) :
        __tmp0.add(e)
        super().visit_cast_expr(e)

    def visit_reveal_type_expr(__tmp0, e: RevealTypeExpr) -> None:
        __tmp0.add(e)
        super().visit_reveal_type_expr(e)

    def visit_unary_expr(__tmp0, e: UnaryExpr) :
        __tmp0.add(e)
        super().visit_unary_expr(e)

    def visit_list_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_list_expr(e)

    def visit_tuple_expr(__tmp0, e: TupleExpr) -> None:
        __tmp0.add(e)
        super().visit_tuple_expr(e)

    def visit_dict_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_dict_expr(e)

    def visit_set_expr(__tmp0, e: SetExpr) -> None:
        __tmp0.add(e)
        super().visit_set_expr(e)

    def visit_index_expr(__tmp0, e: IndexExpr) -> None:
        __tmp0.add(e)
        super().visit_index_expr(e)

    def visit_generator_expr(__tmp0, e) :
        __tmp0.add(e)
        super().visit_generator_expr(e)

    def visit_dictionary_comprehension(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_dictionary_comprehension(e)

    def visit_list_comprehension(__tmp0, e: __typ2) -> None:
        __tmp0.add(e)
        super().visit_list_comprehension(e)

    def visit_set_comprehension(__tmp0, e: SetComprehension) -> None:
        __tmp0.add(e)
        super().visit_set_comprehension(e)

    def visit_conditional_expr(__tmp0, e: ConditionalExpr) -> None:
        __tmp0.add(e)
        super().visit_conditional_expr(e)

    def visit_type_application(__tmp0, e) :
        __tmp0.add(e)
        super().visit_type_application(e)

    def visit_lambda_expr(__tmp0, e: LambdaExpr) -> None:
        __tmp0.add(e)
        super().visit_lambda_expr(e)

    def visit_star_expr(__tmp0, e) -> None:
        __tmp0.add(e)
        super().visit_star_expr(e)

    def visit_backquote_expr(__tmp0, e: BackquoteExpr) :
        __tmp0.add(e)
        super().visit_backquote_expr(e)

    def visit_await_expr(__tmp0, e: AwaitExpr) -> None:
        __tmp0.add(e)
        super().visit_await_expr(e)

    def add(__tmp0, e) -> None:
        __tmp0.expressions.append(e)
