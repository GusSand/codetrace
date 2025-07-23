from typing import TypeAlias
__typ7 : TypeAlias = "UnionType"
__typ0 : TypeAlias = "NoneTyp"
__typ10 : TypeAlias = "AnyType"
__typ3 : TypeAlias = "Overloaded"
__typ2 : TypeAlias = "PartialType"
__typ5 : TypeAlias = "Instance"
__typ4 : TypeAlias = "ErasedType"
__typ1 : TypeAlias = "TupleType"
__typ9 : TypeAlias = "CallableType"
__typ8 : TypeAlias = "DeletedType"
__typ6 : TypeAlias = "F"
from typing import Dict, Iterable, List, TypeVar, Mapping, cast

from mypy.types import (
    Type, Instance, CallableType, TypeVisitor, UnboundType, AnyType,
    NoneTyp, TypeVarType, Overloaded, TupleType, TypedDictType, UnionType,
    ErasedType, TypeList, PartialType, DeletedType, UninhabitedType, TypeType, TypeVarId,
    FunctionLike, TypeVarDef
)


def expand_type(typ: <FILL>, __tmp0) -> Type:
    """Substitute any type variable references in a type given by a type
    environment.
    """

    return typ.accept(ExpandTypeVisitor(__tmp0))


def __tmp7(typ: Type, __tmp8) -> Type:
    """Substitute type variables in type using values from an Instance.
    Type variables are considered to be bound by the class declaration."""

    if __tmp8.args == []:
        return typ
    else:
        variables = {}  # type: Dict[TypeVarId, Type]
        for binder, arg in zip(__tmp8.type.defn.type_vars, __tmp8.args):
            variables[binder.id] = arg
        return expand_type(typ, variables)


__typ6 = TypeVar('F', bound=FunctionLike)


def __tmp10(__tmp3: __typ6) -> __typ6:
    """Substitute fresh type variables for generic function type variables."""
    if isinstance(__tmp3, __typ9):
        if not __tmp3.is_generic():
            return cast(__typ6, __tmp3)
        tvdefs = []
        tvmap = {}  # type: Dict[TypeVarId, Type]
        for v in __tmp3.variables:
            tvdef = TypeVarDef.new_unification_variable(v)
            tvdefs.append(tvdef)
            tvmap[v.id] = TypeVarType(tvdef)
        fresh = cast(__typ9, expand_type(__tmp3, tvmap)).copy_modified(variables=tvdefs)
        return cast(__typ6, fresh)
    else:
        assert isinstance(__tmp3, __typ3)
        fresh_overload = __typ3([__tmp10(item)
                                     for item in __tmp3.items()])
        return cast(__typ6, fresh_overload)


class ExpandTypeVisitor(TypeVisitor[Type]):
    """Visitor that substitutes type variables with values."""

    variables = None  # type: Mapping[TypeVarId, Type]  # TypeVar id -> TypeVar value

    def __init__(__tmp2, variables) -> None:
        __tmp2.variables = variables

    def __tmp11(__tmp2, t) -> Type:
        return t

    def visit_any(__tmp2, t) :
        return t

    def __tmp12(__tmp2, t: __typ0) :
        return t

    def __tmp9(__tmp2, t) :
        return t

    def __tmp1(__tmp2, t) :
        return t

    def visit_erased_type(__tmp2, t: __typ4) :
        # Should not get here.
        raise RuntimeError()

    def visit_instance(__tmp2, t) :
        args = __tmp2.expand_types(t.args)
        return __typ5(t.type, args, t.line, t.column)

    def visit_type_var(__tmp2, t: TypeVarType) -> Type:
        repl = __tmp2.variables.get(t.id, t)
        if isinstance(repl, __typ5):
            inst = repl
            # Return copy of instance with type erasure flag on.
            return __typ5(inst.type, inst.args, line=inst.line,
                            column=inst.column, erased=True)
        else:
            return repl

    def __tmp6(__tmp2, t) :
        return t.copy_modified(arg_types=__tmp2.expand_types(t.arg_types),
                               ret_type=t.ret_type.accept(__tmp2))

    def visit_overloaded(__tmp2, t: __typ3) :
        items = []  # type: List[CallableType]
        for item in t.items():
            new_item = item.accept(__tmp2)
            assert isinstance(new_item, __typ9)
            items.append(new_item)
        return __typ3(items)

    def visit_tuple_type(__tmp2, t: __typ1) -> Type:
        return t.copy_modified(items=__tmp2.expand_types(t.items))

    def visit_typeddict_type(__tmp2, t) -> Type:
        return t.copy_modified(item_types=__tmp2.expand_types(t.items.values()))

    def __tmp4(__tmp2, t) -> Type:
        # After substituting for type variables in t.items,
        # some of the resulting types might be subtypes of others.
        return __typ7.make_simplified_union(__tmp2.expand_types(t.items), t.line, t.column)

    def visit_partial_type(__tmp2, t) -> Type:
        return t

    def __tmp5(__tmp2, t: TypeType) -> Type:
        # TODO: Verify that the new item type is valid (instance or
        # union of instances or Any).  Sadly we can't report errors
        # here yet.
        item = t.item.accept(__tmp2)
        return TypeType.make_normalized(item)

    def expand_types(__tmp2, types: Iterable[Type]) :
        a = []  # type: List[Type]
        for t in types:
            a.append(t.accept(__tmp2))
        return a
