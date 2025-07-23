from typing import TypeAlias
__typ5 : TypeAlias = "TypeType"
__typ1 : TypeAlias = "PartialType"
__typ0 : TypeAlias = "NoneTyp"
__typ2 : TypeAlias = "Type"
__typ6 : TypeAlias = "CallableType"
__typ3 : TypeAlias = "TypeVarType"
from typing import Dict, Iterable, List, TypeVar, Mapping, cast

from mypy.types import (
    Type, Instance, CallableType, TypeVisitor, UnboundType, AnyType,
    NoneTyp, TypeVarType, Overloaded, TupleType, TypedDictType, UnionType,
    ErasedType, TypeList, PartialType, DeletedType, UninhabitedType, TypeType, TypeVarId,
    FunctionLike, TypeVarDef
)


def expand_type(typ: __typ2, env) :
    """Substitute any type variable references in a type given by a type
    environment.
    """

    return typ.accept(__typ4(env))


def expand_type_by_instance(typ, instance: <FILL>) -> __typ2:
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


def __tmp3(callee) :
    """Substitute fresh type variables for generic function type variables."""
    if isinstance(callee, __typ6):
        if not callee.is_generic():
            return cast(F, callee)
        tvdefs = []
        tvmap = {}  # type: Dict[TypeVarId, Type]
        for v in callee.variables:
            tvdef = TypeVarDef.new_unification_variable(v)
            tvdefs.append(tvdef)
            tvmap[v.id] = __typ3(tvdef)
        fresh = cast(__typ6, expand_type(callee, tvmap)).copy_modified(variables=tvdefs)
        return cast(F, fresh)
    else:
        assert isinstance(callee, Overloaded)
        fresh_overload = Overloaded([__tmp3(item)
                                     for item in callee.items()])
        return cast(F, fresh_overload)


class __typ4(TypeVisitor[__typ2]):
    """Visitor that substitutes type variables with values."""

    variables = None  # type: Mapping[TypeVarId, Type]  # TypeVar id -> TypeVar value

    def __tmp5(__tmp2, variables) -> None:
        __tmp2.variables = variables

    def __tmp6(__tmp2, t) :
        return t

    def visit_any(__tmp2, t) :
        return t

    def visit_none_type(__tmp2, t) :
        return t

    def visit_uninhabited_type(__tmp2, t) :
        return t

    def __tmp0(__tmp2, t) :
        return t

    def visit_erased_type(__tmp2, t: ErasedType) :
        # Should not get here.
        raise RuntimeError()

    def visit_instance(__tmp2, t) :
        args = __tmp2.expand_types(t.args)
        return Instance(t.type, args, t.line, t.column)

    def visit_type_var(__tmp2, t: __typ3) :
        repl = __tmp2.variables.get(t.id, t)
        if isinstance(repl, Instance):
            inst = repl
            # Return copy of instance with type erasure flag on.
            return Instance(inst.type, inst.args, line=inst.line,
                            column=inst.column, erased=True)
        else:
            return repl

    def visit_callable_type(__tmp2, t) -> __typ2:
        return t.copy_modified(arg_types=__tmp2.expand_types(t.arg_types),
                               ret_type=t.ret_type.accept(__tmp2))

    def visit_overloaded(__tmp2, t: Overloaded) :
        items = []  # type: List[CallableType]
        for item in t.items():
            new_item = item.accept(__tmp2)
            assert isinstance(new_item, __typ6)
            items.append(new_item)
        return Overloaded(items)

    def visit_tuple_type(__tmp2, t) :
        return t.copy_modified(items=__tmp2.expand_types(t.items))

    def __tmp1(__tmp2, t) :
        return t.copy_modified(item_types=__tmp2.expand_types(t.items.values()))

    def visit_union_type(__tmp2, t) :
        # After substituting for type variables in t.items,
        # some of the resulting types might be subtypes of others.
        return UnionType.make_simplified_union(__tmp2.expand_types(t.items), t.line, t.column)

    def __tmp4(__tmp2, t: __typ1) :
        return t

    def visit_type_type(__tmp2, t) :
        # TODO: Verify that the new item type is valid (instance or
        # union of instances or Any).  Sadly we can't report errors
        # here yet.
        item = t.item.accept(__tmp2)
        return __typ5.make_normalized(item)

    def expand_types(__tmp2, types) :
        a = []  # type: List[Type]
        for t in types:
            a.append(t.accept(__tmp2))
        return a
