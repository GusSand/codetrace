from typing import TypeAlias
__typ0 : TypeAlias = "NoneTyp"
__typ5 : TypeAlias = "TypeType"
__typ1 : TypeAlias = "ErasedType"
__typ2 : TypeAlias = "Instance"
__typ6 : TypeAlias = "UnboundType"
__typ8 : TypeAlias = "CallableType"
__typ3 : TypeAlias = "UninhabitedType"
__typ4 : TypeAlias = "UnionType"
from typing import Optional, Container, Callable

from mypy.types import (
    Type, TypeVisitor, UnboundType, AnyType, NoneTyp, TypeVarId, Instance, TypeVarType,
    CallableType, TupleType, TypedDictType, UnionType, Overloaded, ErasedType, PartialType,
    DeletedType, TypeTranslator, TypeList, UninhabitedType, TypeType, TypeOfAny
)
from mypy import experiments


def erase_type(typ) :
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

    def visit_unbound_type(__tmp1, t) -> Type:
        assert False, 'Not supported'

    def __tmp7(__tmp1, t: AnyType) -> Type:
        return t

    def __tmp11(__tmp1, t: __typ0) :
        return t

    def __tmp4(__tmp1, t: __typ3) :
        return t

    def visit_erased_type(__tmp1, t: __typ1) :
        # Should not get here.
        raise RuntimeError()

    def __tmp6(__tmp1, t: PartialType) :
        # Should not get here.
        raise RuntimeError()

    def visit_deleted_type(__tmp1, t: DeletedType) -> Type:
        return t

    def __tmp10(__tmp1, t: __typ2) :
        return __typ2(t.type, [AnyType(TypeOfAny.special_form)] * len(t.args), t.line)

    def __tmp5(__tmp1, t: TypeVarType) -> Type:
        return AnyType(TypeOfAny.special_form)

    def visit_callable_type(__tmp1, t: __typ8) -> Type:
        # We must preserve the fallback type for overload resolution to work.
        ret_type = __typ0()  # type: Type
        return __typ8([], [], [], ret_type, t.fallback)

    def __tmp8(__tmp1, t: Overloaded) -> Type:
        return t.items()[0].accept(__tmp1)

    def __tmp9(__tmp1, t: TupleType) -> Type:
        return t.fallback.accept(__tmp1)

    def __tmp2(__tmp1, t) -> Type:
        return t.fallback.accept(__tmp1)

    def visit_union_type(__tmp1, t: __typ4) -> Type:
        erased_items = [erase_type(item) for item in t.items]
        return __typ4.make_simplified_union(erased_items)

    def __tmp3(__tmp1, t) -> Type:
        return __typ5.make_normalized(t.item.accept(__tmp1), line=t.line)


def __tmp0(t: <FILL>, ids_to_erase: Optional[Container[TypeVarId]] = None) -> Type:
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """
    def erase_id(id) :
        if ids_to_erase is None:
            return True
        return id in ids_to_erase
    return t.accept(__typ7(erase_id, AnyType(TypeOfAny.special_form)))


def replace_meta_vars(t: Type, target_type: Type) :
    """Replace unification variables in a type with the target type."""
    return t.accept(__typ7(lambda id: id.is_meta_var(), target_type))


class __typ7(TypeTranslator):
    """Implementation of type erasure"""

    def __init__(__tmp1, erase_id: Callable[[TypeVarId], bool], replacement) :
        __tmp1.erase_id = erase_id
        __tmp1.replacement = replacement

    def __tmp5(__tmp1, t) -> Type:
        if __tmp1.erase_id(t.id):
            return __tmp1.replacement
        return t
