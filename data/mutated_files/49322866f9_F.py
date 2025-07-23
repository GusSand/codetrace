from typing import TypeAlias
__typ10 : TypeAlias = "CallableType"
__typ0 : TypeAlias = "NoneTyp"
__typ8 : TypeAlias = "TypeType"
__typ5 : TypeAlias = "UnionType"
__typ2 : TypeAlias = "PartialType"
__typ11 : TypeAlias = "AnyType"
__typ1 : TypeAlias = "TupleType"
__typ9 : TypeAlias = "UnboundType"
__typ6 : TypeAlias = "DeletedType"
__typ4 : TypeAlias = "Instance"
__typ3 : TypeAlias = "Type"
from typing import Dict, Iterable, List, TypeVar, Mapping, cast

from mypy.types import (
    Type, Instance, CallableType, TypeVisitor, UnboundType, AnyType,
    NoneTyp, TypeVarType, Overloaded, TupleType, TypedDictType, UnionType,
    ErasedType, TypeList, PartialType, DeletedType, UninhabitedType, TypeType, TypeVarId,
    FunctionLike, TypeVarDef
)


def expand_type(typ: __typ3, env) -> __typ3:
    """Substitute any type variable references in a type given by a type
    environment.
    """

    return typ.accept(__typ7(env))


def expand_type_by_instance(typ: __typ3, instance: __typ4) :
    """Substitute type variables in type using values from an Instance.
    Type variables are considered to be bound by the class declaration."""

    if instance.args == []:
        return typ
    else:
        variables = {}  # type: Dict[TypeVarId, Type]
        for binder, arg in zip(instance.type.defn.type_vars, instance.args):
            variables[binder.id] = arg
        return expand_type(typ, variables)


F = TypeVar('F', bound=FunctionLike)


def freshen_function_type_vars(__tmp1: <FILL>) -> F:
    """Substitute fresh type variables for generic function type variables."""
    if isinstance(__tmp1, __typ10):
        if not __tmp1.is_generic():
            return cast(F, __tmp1)
        tvdefs = []
        tvmap = {}  # type: Dict[TypeVarId, Type]
        for v in __tmp1.variables:
            tvdef = TypeVarDef.new_unification_variable(v)
            tvdefs.append(tvdef)
            tvmap[v.id] = TypeVarType(tvdef)
        fresh = cast(__typ10, expand_type(__tmp1, tvmap)).copy_modified(variables=tvdefs)
        return cast(F, fresh)
    else:
        assert isinstance(__tmp1, Overloaded)
        fresh_overload = Overloaded([freshen_function_type_vars(item)
                                     for item in __tmp1.items()])
        return cast(F, fresh_overload)


class __typ7(TypeVisitor[__typ3]):
    """Visitor that substitutes type variables with values."""

    variables = None  # type: Mapping[TypeVarId, Type]  # TypeVar id -> TypeVar value

    def __init__(__tmp2, variables: Mapping[TypeVarId, __typ3]) :
        __tmp2.variables = variables

    def visit_unbound_type(__tmp2, t: __typ9) :
        return t

    def __tmp5(__tmp2, t: __typ11) -> __typ3:
        return t

    def visit_none_type(__tmp2, t: __typ0) -> __typ3:
        return t

    def visit_uninhabited_type(__tmp2, t: UninhabitedType) -> __typ3:
        return t

    def visit_deleted_type(__tmp2, t: __typ6) -> __typ3:
        return t

    def __tmp0(__tmp2, t: ErasedType) -> __typ3:
        # Should not get here.
        raise RuntimeError()

    def visit_instance(__tmp2, t: __typ4) :
        args = __tmp2.expand_types(t.args)
        return __typ4(t.type, args, t.line, t.column)

    def __tmp4(__tmp2, t: TypeVarType) :
        repl = __tmp2.variables.get(t.id, t)
        if isinstance(repl, __typ4):
            inst = repl
            # Return copy of instance with type erasure flag on.
            return __typ4(inst.type, inst.args, line=inst.line,
                            column=inst.column, erased=True)
        else:
            return repl

    def visit_callable_type(__tmp2, t: __typ10) -> __typ3:
        return t.copy_modified(arg_types=__tmp2.expand_types(t.arg_types),
                               ret_type=t.ret_type.accept(__tmp2))

    def visit_overloaded(__tmp2, t: Overloaded) -> __typ3:
        items = []  # type: List[CallableType]
        for item in t.items():
            new_item = item.accept(__tmp2)
            assert isinstance(new_item, __typ10)
            items.append(new_item)
        return Overloaded(items)

    def visit_tuple_type(__tmp2, t: __typ1) -> __typ3:
        return t.copy_modified(items=__tmp2.expand_types(t.items))

    def visit_typeddict_type(__tmp2, t: TypedDictType) -> __typ3:
        return t.copy_modified(item_types=__tmp2.expand_types(t.items.values()))

    def visit_union_type(__tmp2, t) -> __typ3:
        # After substituting for type variables in t.items,
        # some of the resulting types might be subtypes of others.
        return __typ5.make_simplified_union(__tmp2.expand_types(t.items), t.line, t.column)

    def visit_partial_type(__tmp2, t) -> __typ3:
        return t

    def __tmp3(__tmp2, t: __typ8) -> __typ3:
        # TODO: Verify that the new item type is valid (instance or
        # union of instances or Any).  Sadly we can't report errors
        # here yet.
        item = t.item.accept(__tmp2)
        return __typ8.make_normalized(item)

    def expand_types(__tmp2, types: Iterable[__typ3]) -> List[__typ3]:
        a = []  # type: List[Type]
        for t in types:
            a.append(t.accept(__tmp2))
        return a
