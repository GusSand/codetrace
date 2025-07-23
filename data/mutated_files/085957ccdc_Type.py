from typing import TypeAlias
__typ2 : TypeAlias = "TypeVarType"
__typ6 : TypeAlias = "UnionType"
__typ8 : TypeAlias = "TypeType"
__typ0 : TypeAlias = "TupleType"
__typ7 : TypeAlias = "DeletedType"
__typ3 : TypeAlias = "UninhabitedType"
__typ11 : TypeAlias = "AnyType"
__typ9 : TypeAlias = "TypeVarId"
__typ5 : TypeAlias = "ErasedType"
__typ4 : TypeAlias = "Instance"
from typing import Optional, Container, Callable

from mypy.types import (
    Type, TypeVisitor, UnboundType, AnyType, NoneTyp, TypeVarId, Instance, TypeVarType,
    CallableType, TupleType, TypedDictType, UnionType, Overloaded, ErasedType, PartialType,
    DeletedType, TypeTranslator, TypeList, UninhabitedType, TypeType, TypeOfAny
)
from mypy import experiments


def erase_type(typ) -> Type:
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

    return typ.accept(__typ1())


class __typ1(TypeVisitor[Type]):

    def __tmp8(__tmp2, t) -> Type:
        assert False, 'Not supported'

    def visit_any(__tmp2, t) -> Type:
        return t

    def __tmp9(__tmp2, t) :
        return t

    def visit_uninhabited_type(__tmp2, t) -> Type:
        return t

    def __tmp0(__tmp2, t) :
        # Should not get here.
        raise RuntimeError()

    def __tmp6(__tmp2, t: PartialType) :
        # Should not get here.
        raise RuntimeError()

    def visit_deleted_type(__tmp2, t) -> Type:
        return t

    def visit_instance(__tmp2, t: __typ4) :
        return __typ4(t.type, [__typ11(TypeOfAny.special_form)] * len(t.args), t.line)

    def __tmp5(__tmp2, t) :
        return __typ11(TypeOfAny.special_form)

    def __tmp4(__tmp2, t) :
        # We must preserve the fallback type for overload resolution to work.
        ret_type = NoneTyp()  # type: Type
        return CallableType([], [], [], ret_type, t.fallback)

    def visit_overloaded(__tmp2, t: Overloaded) :
        return t.items()[0].accept(__tmp2)

    def visit_tuple_type(__tmp2, t) -> Type:
        return t.fallback.accept(__tmp2)

    def __tmp1(__tmp2, t) :
        return t.fallback.accept(__tmp2)

    def visit_union_type(__tmp2, t: __typ6) :
        erased_items = [erase_type(item) for item in t.items]
        return __typ6.make_simplified_union(erased_items)

    def __tmp3(__tmp2, t: __typ8) -> Type:
        return __typ8.make_normalized(t.item.accept(__tmp2), line=t.line)


def erase_typevars(t: Type, ids_to_erase: Optional[Container[__typ9]] = None) -> Type:
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """
    def erase_id(id) :
        if ids_to_erase is None:
            return True
        return id in ids_to_erase
    return t.accept(__typ10(erase_id, __typ11(TypeOfAny.special_form)))


def __tmp10(t: Type, __tmp7: <FILL>) -> Type:
    """Replace unification variables in a type with the target type."""
    return t.accept(__typ10(lambda id: id.is_meta_var(), __tmp7))


class __typ10(TypeTranslator):
    """Implementation of type erasure"""

    def __init__(__tmp2, erase_id, replacement: Type) :
        __tmp2.erase_id = erase_id
        __tmp2.replacement = replacement

    def __tmp5(__tmp2, t: __typ2) :
        if __tmp2.erase_id(t.id):
            return __tmp2.replacement
        return t
