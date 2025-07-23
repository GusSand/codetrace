from typing import TypeAlias
__typ1 : TypeAlias = "Instance"
__typ2 : TypeAlias = "DeletedType"
__typ0 : TypeAlias = "Overloaded"
__typ4 : TypeAlias = "CallableType"
__typ3 : TypeAlias = "UnionType"
from typing import Dict, Iterable, List, TypeVar, Mapping, cast

from mypy.types import (
    Type, Instance, CallableType, TypeVisitor, UnboundType, AnyType,
    NoneTyp, TypeVarType, Overloaded, TupleType, TypedDictType, UnionType,
    ErasedType, TypeList, PartialType, DeletedType, UninhabitedType, TypeType, TypeVarId,
    FunctionLike, TypeVarDef
)


def expand_type(typ: Type, env: Mapping[TypeVarId, Type]) :
    """Substitute any type variable references in a type given by a type
    environment.
    """

    return typ.accept(ExpandTypeVisitor(env))


def expand_type_by_instance(typ: <FILL>, instance: __typ1) -> Type:
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


def freshen_function_type_vars(callee: F) -> F:
    """Substitute fresh type variables for generic function type variables."""
    if isinstance(callee, __typ4):
        if not callee.is_generic():
            return cast(F, callee)
        tvdefs = []
        tvmap = {}  # type: Dict[TypeVarId, Type]
        for v in callee.variables:
            tvdef = TypeVarDef.new_unification_variable(v)
            tvdefs.append(tvdef)
            tvmap[v.id] = TypeVarType(tvdef)
        fresh = cast(__typ4, expand_type(callee, tvmap)).copy_modified(variables=tvdefs)
        return cast(F, fresh)
    else:
        assert isinstance(callee, __typ0)
        fresh_overload = __typ0([freshen_function_type_vars(item)
                                     for item in callee.items()])
        return cast(F, fresh_overload)


class ExpandTypeVisitor(TypeVisitor[Type]):
    """Visitor that substitutes type variables with values."""

    variables = None  # type: Mapping[TypeVarId, Type]  # TypeVar id -> TypeVar value

    def __init__(self, variables: Mapping[TypeVarId, Type]) -> None:
        self.variables = variables

    def visit_unbound_type(self, t: UnboundType) :
        return t

    def visit_any(self, t) :
        return t

    def visit_none_type(self, t: NoneTyp) -> Type:
        return t

    def visit_uninhabited_type(self, t: UninhabitedType) -> Type:
        return t

    def visit_deleted_type(self, t) -> Type:
        return t

    def visit_erased_type(self, t) -> Type:
        # Should not get here.
        raise RuntimeError()

    def __tmp0(self, t: __typ1) -> Type:
        args = self.expand_types(t.args)
        return __typ1(t.type, args, t.line, t.column)

    def visit_type_var(self, t) :
        repl = self.variables.get(t.id, t)
        if isinstance(repl, __typ1):
            inst = repl
            # Return copy of instance with type erasure flag on.
            return __typ1(inst.type, inst.args, line=inst.line,
                            column=inst.column, erased=True)
        else:
            return repl

    def visit_callable_type(self, t) -> Type:
        return t.copy_modified(arg_types=self.expand_types(t.arg_types),
                               ret_type=t.ret_type.accept(self))

    def visit_overloaded(self, t: __typ0) -> Type:
        items = []  # type: List[CallableType]
        for item in t.items():
            new_item = item.accept(self)
            assert isinstance(new_item, __typ4)
            items.append(new_item)
        return __typ0(items)

    def visit_tuple_type(self, t: TupleType) -> Type:
        return t.copy_modified(items=self.expand_types(t.items))

    def visit_typeddict_type(self, t: TypedDictType) -> Type:
        return t.copy_modified(item_types=self.expand_types(t.items.values()))

    def visit_union_type(self, t: __typ3) -> Type:
        # After substituting for type variables in t.items,
        # some of the resulting types might be subtypes of others.
        return __typ3.make_simplified_union(self.expand_types(t.items), t.line, t.column)

    def visit_partial_type(self, t: PartialType) :
        return t

    def visit_type_type(self, t: TypeType) -> Type:
        # TODO: Verify that the new item type is valid (instance or
        # union of instances or Any).  Sadly we can't report errors
        # here yet.
        item = t.item.accept(self)
        return TypeType.make_normalized(item)

    def expand_types(self, types: Iterable[Type]) -> List[Type]:
        a = []  # type: List[Type]
        for t in types:
            a.append(t.accept(self))
        return a
