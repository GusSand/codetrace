"""Utilities for type argument inference."""

from typing import List, Optional, Sequence

from mypy.constraints import infer_constraints, infer_constraints_for_callable
from mypy.types import Type, TypeVarId, CallableType
from mypy.solve import solve_constraints
from mypy.constraints import SUBTYPE_OF


def infer_function_type_arguments(__tmp2,
                                  __tmp0,
                                  __tmp3,
                                  __tmp1,
                                  strict: bool = True) :
    """Infer the type arguments of a generic function.

    Return an array of lower bound types for the type variables -1 (at
    index 0), -2 (at index 1), etc. A lower bound is None if a value
    could not be inferred.

    Arguments:
      callee_type: the target generic function
      arg_types: argument types at the call site (each optional; if None,
                 we are not considering this argument in the current pass)
      arg_kinds: nodes.ARG_* values for arg_types
      formal_to_actual: mapping from formal to actual variable indices
    """
    # Infer constraints.
    constraints = infer_constraints_for_callable(
        __tmp2, __tmp0, __tmp3, __tmp1)

    # Solve constraints.
    type_vars = __tmp2.type_var_ids()
    return solve_constraints(type_vars, constraints, strict)


def infer_type_arguments(type_var_ids,
                         template, __tmp4: <FILL>) :
    # Like infer_function_type_arguments, but only match a single type
    # against a generic type.
    constraints = infer_constraints(template, __tmp4, SUBTYPE_OF)
    return solve_constraints(type_var_ids, constraints)
