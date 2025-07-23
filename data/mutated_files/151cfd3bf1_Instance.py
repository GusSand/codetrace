from typing import TypeAlias
__typ0 : TypeAlias = "NoneTyp"
__typ13 : TypeAlias = "DeletedType"
__typ7 : TypeAlias = "TypeVarType"
__typ3 : TypeAlias = "Overloaded"
__typ5 : TypeAlias = "Type"
__typ14 : TypeAlias = "UnboundType"
__typ8 : TypeAlias = "UninhabitedType"
__typ10 : TypeAlias = "F"
__typ4 : TypeAlias = "PartialType"
__typ6 : TypeAlias = "ErasedType"
__typ1 : TypeAlias = "TupleType"
__typ12 : TypeAlias = "TypeType"
__typ9 : TypeAlias = "UnionType"
__typ16 : TypeAlias = "AnyType"
__typ15 : TypeAlias = "CallableType"
__typ2 : TypeAlias = "TypedDictType"
from typing import Dict, Iterable, List, TypeVar, Mapping, cast

from mypy.types import (
    Type, Instance, CallableType, TypeVisitor, UnboundType, AnyType,
    NoneTyp, TypeVarType, Overloaded, TupleType, TypedDictType, UnionType,
    ErasedType, TypeList, PartialType, DeletedType, UninhabitedType, TypeType, TypeVarId,
    FunctionLike, TypeVarDef
)


def expand_type(typ: __typ5, env) -> __typ5:
    """Substitute any type variable references in a type given by a type
    environment.
    """

    return typ.accept(__typ11(env))


def expand_type_by_instance(typ, instance) :
    """Substitute type variables in type using values from an Instance.
    Type variables are considered to be bound by the class declaration."""

    if instance.args == []:
        return typ
    else:
        variables = {}  # type: Dict[TypeVarId, Type]
        for binder, arg in zip(instance.type.defn.type_vars, instance.args):
            variables[binder.id] = arg
        return expand_type(typ, variables)


__typ10 = TypeVar('F', bound=FunctionLike)


def freshen_function_type_vars(callee) :
    """Substitute fresh type variables for generic function type variables."""
    if isinstance(callee, __typ15):
        if not callee.is_generic():
            return cast(__typ10, callee)
        tvdefs = []
        tvmap = {}  # type: Dict[TypeVarId, Type]
        for v in callee.variables:
            tvdef = TypeVarDef.new_unification_variable(v)
            tvdefs.append(tvdef)
            tvmap[v.id] = __typ7(tvdef)
        fresh = cast(__typ15, expand_type(callee, tvmap)).copy_modified(variables=tvdefs)
        return cast(__typ10, fresh)
    else:
        assert isinstance(callee, __typ3)
        fresh_overload = __typ3([freshen_function_type_vars(item)
                                     for item in callee.items()])
        return cast(__typ10, fresh_overload)


class __typ11(TypeVisitor[__typ5]):
    """Visitor that substitutes type variables with values."""

    variables = None  # type: Mapping[TypeVarId, Type]  # TypeVar id -> TypeVar value

    def __init__(__tmp1, variables: Mapping[TypeVarId, __typ5]) :
        __tmp1.variables = variables

    def visit_unbound_type(__tmp1, t: __typ14) :
        return t

    def visit_any(__tmp1, t: __typ16) -> __typ5:
        return t

    def __tmp0(__tmp1, t) :
        return t

    def visit_uninhabited_type(__tmp1, t) -> __typ5:
        return t

    def visit_deleted_type(__tmp1, t) :
        return t

    def visit_erased_type(__tmp1, t) -> __typ5:
        # Should not get here.
        raise RuntimeError()

    def visit_instance(__tmp1, t: <FILL>) :
        args = __tmp1.expand_types(t.args)
        return Instance(t.type, args, t.line, t.column)

    def visit_type_var(__tmp1, t) -> __typ5:
        repl = __tmp1.variables.get(t.id, t)
        if isinstance(repl, Instance):
            inst = repl
            # Return copy of instance with type erasure flag on.
            return Instance(inst.type, inst.args, line=inst.line,
                            column=inst.column, erased=True)
        else:
            return repl

    def visit_callable_type(__tmp1, t) -> __typ5:
        return t.copy_modified(arg_types=__tmp1.expand_types(t.arg_types),
                               ret_type=t.ret_type.accept(__tmp1))

    def visit_overloaded(__tmp1, t) -> __typ5:
        items = []  # type: List[CallableType]
        for item in t.items():
            new_item = item.accept(__tmp1)
            assert isinstance(new_item, __typ15)
            items.append(new_item)
        return __typ3(items)

    def visit_tuple_type(__tmp1, t: __typ1) :
        return t.copy_modified(items=__tmp1.expand_types(t.items))

    def visit_typeddict_type(__tmp1, t) -> __typ5:
        return t.copy_modified(item_types=__tmp1.expand_types(t.items.values()))

    def __tmp3(__tmp1, t) :
        # After substituting for type variables in t.items,
        # some of the resulting types might be subtypes of others.
        return __typ9.make_simplified_union(__tmp1.expand_types(t.items), t.line, t.column)

    def visit_partial_type(__tmp1, t) :
        return t

    def __tmp2(__tmp1, t) -> __typ5:
        # TODO: Verify that the new item type is valid (instance or
        # union of instances or Any).  Sadly we can't report errors
        # here yet.
        item = t.item.accept(__tmp1)
        return __typ12.make_normalized(item)

    def expand_types(__tmp1, types: Iterable[__typ5]) :
        a = []  # type: List[Type]
        for t in types:
            a.append(t.accept(__tmp1))
        return a
