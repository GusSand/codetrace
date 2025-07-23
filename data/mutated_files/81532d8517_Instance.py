from typing import TypeAlias
__typ2 : TypeAlias = "Type"
__typ0 : TypeAlias = "Overloaded"
from typing import Optional, Container, Callable

from mypy.types import (
    Type, TypeVisitor, UnboundType, AnyType, NoneTyp, TypeVarId, Instance, TypeVarType,
    CallableType, TupleType, TypedDictType, UnionType, Overloaded, ErasedType, PartialType,
    DeletedType, TypeTranslator, TypeList, UninhabitedType, TypeType, TypeOfAny
)
from mypy import experiments


def __tmp3(typ) :
    """Erase any type variables from a type.

    Also replace tuple types with the corresponding concrete types. Replace
    callable types with empty callable types.

    Examples:
      A -> A
      B[X] -> B[Any]
      Tuple[A, B] -> tuple
      Callable[...] -> Callable[[], None]
      Type[X] -> Type[Any]
    """

    return typ.accept(EraseTypeVisitor())


class EraseTypeVisitor(TypeVisitor[__typ2]):

    def visit_unbound_type(__tmp1, t: UnboundType) -> __typ2:
        assert False, 'Not supported'

    def __tmp5(__tmp1, t: AnyType) :
        return t

    def visit_none_type(__tmp1, t) :
        return t

    def __tmp2(__tmp1, t) :
        return t

    def __tmp0(__tmp1, t) -> __typ2:
        # Should not get here.
        raise RuntimeError()

    def visit_partial_type(__tmp1, t: PartialType) -> __typ2:
        # Should not get here.
        raise RuntimeError()

    def visit_deleted_type(__tmp1, t: DeletedType) :
        return t

    def __tmp9(__tmp1, t: <FILL>) :
        return Instance(t.type, [AnyType(TypeOfAny.special_form)] * len(t.args), t.line)

    def __tmp4(__tmp1, t) :
        return AnyType(TypeOfAny.special_form)

    def visit_callable_type(__tmp1, t) :
        # We must preserve the fallback type for overload resolution to work.
        ret_type = NoneTyp()  # type: Type
        return CallableType([], [], [], ret_type, t.fallback)

    def __tmp8(__tmp1, t) -> __typ2:
        return t.items()[0].accept(__tmp1)

    def __tmp6(__tmp1, t) :
        return t.fallback.accept(__tmp1)

    def visit_typeddict_type(__tmp1, t) -> __typ2:
        return t.fallback.accept(__tmp1)

    def visit_union_type(__tmp1, t) -> __typ2:
        erased_items = [__tmp3(item) for item in t.items]
        return UnionType.make_simplified_union(erased_items)

    def visit_type_type(__tmp1, t) -> __typ2:
        return TypeType.make_normalized(t.item.accept(__tmp1), line=t.line)


def erase_typevars(t: __typ2, ids_to_erase: Optional[Container[TypeVarId]] = None) :
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """
    def erase_id(id) -> bool:
        if ids_to_erase is None:
            return True
        return id in ids_to_erase
    return t.accept(__typ1(erase_id, AnyType(TypeOfAny.special_form)))


def replace_meta_vars(t, __tmp7: __typ2) -> __typ2:
    """Replace unification variables in a type with the target type."""
    return t.accept(__typ1(lambda id: id.is_meta_var(), __tmp7))


class __typ1(TypeTranslator):
    """Implementation of type erasure"""

    def __init__(__tmp1, erase_id: Callable[[TypeVarId], bool], replacement) :
        __tmp1.erase_id = erase_id
        __tmp1.replacement = replacement

    def __tmp4(__tmp1, t) :
        if __tmp1.erase_id(t.id):
            return __tmp1.replacement
        return t
