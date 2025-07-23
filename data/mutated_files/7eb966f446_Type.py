from typing import TypeAlias
__typ6 : TypeAlias = "TypeVarId"
__typ2 : TypeAlias = "Instance"
__typ0 : TypeAlias = "TupleType"
__typ1 : TypeAlias = "TypeVarType"
__typ3 : TypeAlias = "UnionType"
__typ4 : TypeAlias = "DeletedType"
__typ5 : TypeAlias = "UnboundType"
from typing import Optional, Container, Callable

from mypy.types import (
    Type, TypeVisitor, UnboundType, AnyType, NoneTyp, TypeVarId, Instance, TypeVarType,
    CallableType, TupleType, TypedDictType, UnionType, Overloaded, ErasedType, PartialType,
    DeletedType, TypeTranslator, TypeList, UninhabitedType, TypeType, TypeOfAny
)
from mypy import experiments


def __tmp7(typ) :
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


class EraseTypeVisitor(TypeVisitor[Type]):

    def __tmp14(__tmp3, t) :
        assert False, 'Not supported'

    def __tmp11(__tmp3, t) :
        return t

    def __tmp16(__tmp3, t) :
        return t

    def __tmp8(__tmp3, t) :
        return t

    def __tmp0(__tmp3, t: ErasedType) :
        # Should not get here.
        raise RuntimeError()

    def visit_partial_type(__tmp3, t) :
        # Should not get here.
        raise RuntimeError()

    def __tmp1(__tmp3, t) :
        return t

    def __tmp15(__tmp3, t) -> Type:
        return __typ2(t.type, [AnyType(TypeOfAny.special_form)] * len(t.args), t.line)

    def __tmp9(__tmp3, t) :
        return AnyType(TypeOfAny.special_form)

    def __tmp6(__tmp3, t) :
        # We must preserve the fallback type for overload resolution to work.
        ret_type = NoneTyp()  # type: Type
        return CallableType([], [], [], ret_type, t.fallback)

    def visit_overloaded(__tmp3, t) :
        return t.items()[0].accept(__tmp3)

    def __tmp13(__tmp3, t) :
        return t.fallback.accept(__tmp3)

    def __tmp2(__tmp3, t) :
        return t.fallback.accept(__tmp3)

    def __tmp5(__tmp3, t) :
        erased_items = [__tmp7(item) for item in t.items]
        return __typ3.make_simplified_union(erased_items)

    def __tmp4(__tmp3, t) :
        return TypeType.make_normalized(t.item.accept(__tmp3), line=t.line)


def erase_typevars(t, ids_to_erase: Optional[Container[__typ6]] = None) :
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """
    def erase_id(id) :
        if ids_to_erase is None:
            return True
        return id in ids_to_erase
    return t.accept(TypeVarEraser(erase_id, AnyType(TypeOfAny.special_form)))


def __tmp17(t: <FILL>, __tmp12) :
    """Replace unification variables in a type with the target type."""
    return t.accept(TypeVarEraser(lambda id: id.is_meta_var(), __tmp12))


class TypeVarEraser(TypeTranslator):
    """Implementation of type erasure"""

    def __tmp10(__tmp3, erase_id, replacement) :
        __tmp3.erase_id = erase_id
        __tmp3.replacement = replacement

    def __tmp9(__tmp3, t) :
        if __tmp3.erase_id(t.id):
            return __tmp3.replacement
        return t
