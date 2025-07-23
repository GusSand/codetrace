from typing import TypeAlias
__typ6 : TypeAlias = "PartialType"
__typ2 : TypeAlias = "TupleType"
__typ0 : TypeAlias = "NoneTyp"
__typ16 : TypeAlias = "TypeVarId"
__typ3 : TypeAlias = "TypedDictType"
__typ13 : TypeAlias = "DeletedType"
__typ8 : TypeAlias = "UninhabitedType"
__typ5 : TypeAlias = "Overloaded"
__typ17 : TypeAlias = "AnyType"
__typ14 : TypeAlias = "TypeType"
__typ7 : TypeAlias = "ErasedType"
__typ9 : TypeAlias = "TypeVarType"
__typ12 : TypeAlias = "UnionType"
__typ11 : TypeAlias = "bool"
__typ15 : TypeAlias = "UnboundType"
__typ10 : TypeAlias = "Instance"
from typing import Optional, Container, Callable

from mypy.types import (
    Type, TypeVisitor, UnboundType, AnyType, NoneTyp, TypeVarId, Instance, TypeVarType,
    CallableType, TupleType, TypedDictType, UnionType, Overloaded, ErasedType, PartialType,
    DeletedType, TypeTranslator, TypeList, UninhabitedType, TypeType, TypeOfAny
)
from mypy import experiments


def __tmp15(typ: Type) -> Type:
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

    return typ.accept(__typ4())


class __typ4(TypeVisitor[Type]):

    def __tmp19(__tmp2, t) :
        assert False, 'Not supported'

    def visit_any(__tmp2, t: __typ17) :
        return t

    def __tmp13(__tmp2, t: __typ0) -> Type:
        return t

    def __tmp4(__tmp2, t: __typ8) -> Type:
        return t

    def __tmp0(__tmp2, t) -> Type:
        # Should not get here.
        raise RuntimeError()

    def __tmp17(__tmp2, t: __typ6) :
        # Should not get here.
        raise RuntimeError()

    def __tmp8(__tmp2, t) -> Type:
        return t

    def __tmp6(__tmp2, t: __typ10) -> Type:
        return __typ10(t.type, [__typ17(TypeOfAny.special_form)] * len(t.args), t.line)

    def __tmp16(__tmp2, t: __typ9) -> Type:
        return __typ17(TypeOfAny.special_form)

    def __tmp14(__tmp2, t) :
        # We must preserve the fallback type for overload resolution to work.
        ret_type = __typ0()  # type: Type
        return CallableType([], [], [], ret_type, t.fallback)

    def __tmp5(__tmp2, t) :
        return t.items()[0].accept(__tmp2)

    def __tmp18(__tmp2, t: __typ2) :
        return t.fallback.accept(__tmp2)

    def __tmp10(__tmp2, t: __typ3) -> Type:
        return t.fallback.accept(__tmp2)

    def __tmp3(__tmp2, t) -> Type:
        erased_items = [__tmp15(item) for item in t.items]
        return __typ12.make_simplified_union(erased_items)

    def __tmp11(__tmp2, t: __typ14) -> Type:
        return __typ14.make_normalized(t.item.accept(__tmp2), line=t.line)


def __tmp1(t: Type, ids_to_erase: Optional[Container[__typ16]] = None) -> Type:
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """
    def erase_id(id: __typ16) :
        if ids_to_erase is None:
            return True
        return id in ids_to_erase
    return t.accept(__typ1(erase_id, __typ17(TypeOfAny.special_form)))


def __tmp7(t, __tmp9) -> Type:
    """Replace unification variables in a type with the target type."""
    return t.accept(__typ1(lambda id: id.is_meta_var(), __tmp9))


class __typ1(TypeTranslator):
    """Implementation of type erasure"""

    def __tmp12(__tmp2, erase_id: Callable[[__typ16], __typ11], replacement: <FILL>) -> None:
        __tmp2.erase_id = erase_id
        __tmp2.replacement = replacement

    def __tmp16(__tmp2, t: __typ9) :
        if __tmp2.erase_id(t.id):
            return __tmp2.replacement
        return t
