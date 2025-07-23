from typing import TypeAlias
__typ14 : TypeAlias = "AnyType"
__typ0 : TypeAlias = "NoneTyp"
__typ12 : TypeAlias = "UnboundType"
__typ8 : TypeAlias = "UninhabitedType"
__typ6 : TypeAlias = "Instance"
__typ5 : TypeAlias = "TypeVarType"
__typ1 : TypeAlias = "TupleType"
__typ10 : TypeAlias = "DeletedType"
__typ9 : TypeAlias = "ErasedType"
__typ4 : TypeAlias = "Overloaded"
__typ7 : TypeAlias = "TypeVarId"
__typ11 : TypeAlias = "TypeType"
__typ2 : TypeAlias = "TypedDictType"
from typing import Optional, Container, Callable

from mypy.types import (
    Type, TypeVisitor, UnboundType, AnyType, NoneTyp, TypeVarId, Instance, TypeVarType,
    CallableType, TupleType, TypedDictType, UnionType, Overloaded, ErasedType, PartialType,
    DeletedType, TypeTranslator, TypeList, UninhabitedType, TypeType, TypeOfAny
)
from mypy import experiments


def erase_type(typ: <FILL>) :
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

    return typ.accept(__typ3())


class __typ3(TypeVisitor[Type]):

    def __tmp3(__tmp0, t) :
        assert False, 'Not supported'

    def visit_any(__tmp0, t) :
        return t

    def __tmp4(__tmp0, t) :
        return t

    def __tmp2(__tmp0, t: __typ8) :
        return t

    def visit_erased_type(__tmp0, t) :
        # Should not get here.
        raise RuntimeError()

    def visit_partial_type(__tmp0, t) :
        # Should not get here.
        raise RuntimeError()

    def visit_deleted_type(__tmp0, t) :
        return t

    def visit_instance(__tmp0, t) :
        return __typ6(t.type, [__typ14(TypeOfAny.special_form)] * len(t.args), t.line)

    def visit_type_var(__tmp0, t) :
        return __typ14(TypeOfAny.special_form)

    def __tmp1(__tmp0, t) -> Type:
        # We must preserve the fallback type for overload resolution to work.
        ret_type = __typ0()  # type: Type
        return CallableType([], [], [], ret_type, t.fallback)

    def visit_overloaded(__tmp0, t) :
        return t.items()[0].accept(__tmp0)

    def visit_tuple_type(__tmp0, t: __typ1) :
        return t.fallback.accept(__tmp0)

    def visit_typeddict_type(__tmp0, t) :
        return t.fallback.accept(__tmp0)

    def visit_union_type(__tmp0, t) :
        erased_items = [erase_type(item) for item in t.items]
        return UnionType.make_simplified_union(erased_items)

    def visit_type_type(__tmp0, t) :
        return __typ11.make_normalized(t.item.accept(__tmp0), line=t.line)


def erase_typevars(t, ids_to_erase: Optional[Container[__typ7]] = None) :
    """Replace all type variables in a type with any,
    or just the ones in the provided collection.
    """
    def erase_id(id) :
        if ids_to_erase is None:
            return True
        return id in ids_to_erase
    return t.accept(__typ13(erase_id, __typ14(TypeOfAny.special_form)))


def replace_meta_vars(t, target_type) :
    """Replace unification variables in a type with the target type."""
    return t.accept(__typ13(lambda id: id.is_meta_var(), target_type))


class __typ13(TypeTranslator):
    """Implementation of type erasure"""

    def __init__(__tmp0, erase_id, replacement) :
        __tmp0.erase_id = erase_id
        __tmp0.replacement = replacement

    def visit_type_var(__tmp0, t) :
        if __tmp0.erase_id(t.id):
            return __tmp0.replacement
        return t
