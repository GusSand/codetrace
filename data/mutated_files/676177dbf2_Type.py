from typing import TypeAlias
__typ0 : TypeAlias = "TypeVarType"
"""Test cases for the constraint solver used in type inference."""

from typing import List, Union, Tuple, Optional

from mypy.test.helpers import Suite, assert_equal
from mypy.constraints import SUPERTYPE_OF, SUBTYPE_OF, Constraint
from mypy.solve import solve_constraints
from mypy.test.typefixture import TypeFixture
from mypy.types import Type, TypeVarType, TypeVarId


class SolveSuite(Suite):
    def setUp(__tmp0) :
        __tmp0.fx = TypeFixture()

    def test_empty_input(__tmp0) :
        __tmp0.assert_solve([], [], [])

    def test_simple_supertype_constraints(__tmp0) :
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.a)],
                          [(__tmp0.fx.a, __tmp0.fx.o)])
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.a),
                           __tmp0.supc(__tmp0.fx.t, __tmp0.fx.b)],
                          [(__tmp0.fx.a, __tmp0.fx.o)])

    def test_simple_subtype_constraints(__tmp0) :
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.subc(__tmp0.fx.t, __tmp0.fx.a)],
                          [__tmp0.fx.a])
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.subc(__tmp0.fx.t, __tmp0.fx.a),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.b)],
                          [__tmp0.fx.b])

    def test_both_kinds_of_constraints(__tmp0) -> None:
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.b),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.a)],
                          [(__tmp0.fx.b, __tmp0.fx.a)])

    def test_unsatisfiable_constraints(__tmp0) :
        # The constraints are impossible to satisfy.
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.a),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.b)],
                          [None])

    def test_exactly_specified_result(__tmp0) -> None:
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.b),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.b)],
                          [(__tmp0.fx.b, __tmp0.fx.b)])

    def test_multiple_variables(__tmp0) :
        __tmp0.assert_solve([__tmp0.fx.t.id, __tmp0.fx.s.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.b),
                           __tmp0.supc(__tmp0.fx.s, __tmp0.fx.c),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.a)],
                          [(__tmp0.fx.b, __tmp0.fx.a), (__tmp0.fx.c, __tmp0.fx.o)])

    def test_no_constraints_for_var(__tmp0) :
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [],
                          [__tmp0.fx.uninhabited])
        __tmp0.assert_solve([__tmp0.fx.t.id, __tmp0.fx.s.id],
                          [],
                          [__tmp0.fx.uninhabited, __tmp0.fx.uninhabited])
        __tmp0.assert_solve([__tmp0.fx.t.id, __tmp0.fx.s.id],
                          [__tmp0.supc(__tmp0.fx.s, __tmp0.fx.a)],
                          [__tmp0.fx.uninhabited, (__tmp0.fx.a, __tmp0.fx.o)])

    def test_simple_constraints_with_dynamic_type(__tmp0) :
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.anyt)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.anyt),
                           __tmp0.supc(__tmp0.fx.t, __tmp0.fx.anyt)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.anyt),
                           __tmp0.supc(__tmp0.fx.t, __tmp0.fx.a)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])

        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.subc(__tmp0.fx.t, __tmp0.fx.anyt)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.subc(__tmp0.fx.t, __tmp0.fx.anyt),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.anyt)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])
        # self.assert_solve([self.fx.t.id],
        #                   [self.subc(self.fx.t, self.fx.anyt),
        #                    self.subc(self.fx.t, self.fx.a)],
        #                   [(self.fx.anyt, self.fx.anyt)])
        # TODO: figure out what this should be after changes to meet(any, X)

    def test_both_normal_and_any_types_in_results(__tmp0) :
        # If one of the bounds is any, we promote the other bound to
        # any as well, since otherwise the type range does not make sense.
        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.a),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.anyt)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])

        __tmp0.assert_solve([__tmp0.fx.t.id],
                          [__tmp0.supc(__tmp0.fx.t, __tmp0.fx.anyt),
                           __tmp0.subc(__tmp0.fx.t, __tmp0.fx.a)],
                          [(__tmp0.fx.anyt, __tmp0.fx.anyt)])

    def assert_solve(__tmp0,
                     vars,
                     constraints,
                     results,
                     ) -> None:
        res = []  # type: List[Optional[Type]]
        for r in results:
            if isinstance(r, tuple):
                res.append(r[0])
            else:
                res.append(r)
        actual = solve_constraints(vars, constraints)
        assert_equal(str(actual), str(res))

    def supc(__tmp0, type_var, bound: <FILL>) :
        return Constraint(type_var.id, SUPERTYPE_OF, bound)

    def subc(__tmp0, type_var: __typ0, bound: Type) -> Constraint:
        return Constraint(type_var.id, SUBTYPE_OF, bound)
