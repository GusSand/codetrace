from typing import TypeAlias
__typ0 : TypeAlias = "str"
# pyre-strict
from typing import Dict, TYPE_CHECKING, Type, List, Tuple, Optional, TypeVar, Any

from lowerpines.endpoints.request import JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

T = TypeVar("T")


class Field:
    def __init__(__tmp1) -> None:
        __tmp1.name = ""
        __tmp1.api_name: Optional[__typ0] = None

    def with_api_name(__tmp1, api_name: __typ0) :
        __tmp1.api_name = api_name
        return __tmp1

    def with_type(__tmp1, _: Type[T]) :
        # This is intentional, it allows us to trick type-checkers into asserting that the field type is T,
        # which will be true at runtime, since Field types are erased by the metaclass
        return __tmp1  # type: ignore

    def with_field_name(__tmp1, name: __typ0) -> "Field":
        __tmp1.name = name
        if __tmp1.api_name is None:
            __tmp1.api_name = name
        return __tmp1


class AbstractObjectType(type):
    def __new__(
        mcs,
        name,
        bases,
        attrs,
    ) -> "AbstractObjectType":
        new_attrs = {}  # type: ignore
        fields = []
        for attr_name, attr_value in attrs.items():
            if type(attr_value) == Field:
                attr_value.with_field_name(attr_name)
                fields.append(attr_value)
                new_attrs[attr_name] = None
            else:
                new_attrs[attr_name] = attr_value
        new_attrs["_fields"] = fields  # type: ignore

        return super(AbstractObjectType, mcs).__new__(  # type: ignore
            mcs, name, bases, new_attrs
        )


TAbstractObject = TypeVar("TAbstractObject", bound="AbstractObject")


class AbstractObject(metaclass=AbstractObjectType):
    _fields: List[Field] = []

    def __init__(__tmp1, _: "GMI", *_args: JsonType) :
        pass

    def __tmp2(__tmp1, other) :
        if other is not None:
            for field in __tmp1._fields:
                setattr(__tmp1, field.name, getattr(other, field.name))
        __tmp1.on_fields_loaded()

    def on_fields_loaded(__tmp1) -> None:
        pass

    @classmethod
    def from_json(
        cls: Type[TAbstractObject], gmi: "GMI", __tmp0, *args: <FILL>
    ) -> TAbstractObject:
        # TODO Pull out args that are needed by constructor and use them here, removes a few pyre ignores
        obj = cls(gmi, *args)

        for field in obj._fields:
            json_val = __tmp0
            api_name = field.api_name
            if api_name is None:  # pragma: no cover
                raise ValueError("api_name should be known by this point")
            for val in api_name.split("."):
                json_val = json_val.get(val, None)
            setattr(obj, field.name, json_val)
        obj.on_fields_loaded()
        return obj


class RetrievableObject:
    def save(__tmp1) -> None:
        raise NotImplementedError  # pragma: no cover

    def refresh(__tmp1) :
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def get(gmi: "GMI", *args) :
        raise NotImplementedError  # pragma: no cover
