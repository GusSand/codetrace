# pyre-strict
from typing import Dict, TYPE_CHECKING, Type, List, Tuple, Optional, TypeVar, Any

from lowerpines.endpoints.request import JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

T = TypeVar("T")


class Field:
    def __init__(__tmp3) :
        __tmp3.name = ""
        __tmp3.api_name: Optional[str] = None

    def __tmp4(__tmp3, api_name) :
        __tmp3.api_name = api_name
        return __tmp3

    def __tmp2(__tmp3, _) :
        # This is intentional, it allows us to trick type-checkers into asserting that the field type is T,
        # which will be true at runtime, since Field types are erased by the metaclass
        return __tmp3  # type: ignore

    def with_field_name(__tmp3, name: <FILL>) -> "Field":
        __tmp3.name = name
        if __tmp3.api_name is None:
            __tmp3.api_name = name
        return __tmp3


class AbstractObjectType(type):
    def __new__(
        mcs,
        name: str,
        bases: Tuple[Type["AbstractObjectType"]],
        attrs: Dict[str, Field],
    ) :
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


__typ0 = TypeVar("TAbstractObject", bound="AbstractObject")


class AbstractObject(metaclass=AbstractObjectType):
    _fields: List[Field] = []

    def __init__(__tmp3, _, *_args) :
        pass

    def _refresh_from_other(__tmp3, other: __typ0) -> None:
        if other is not None:
            for field in __tmp3._fields:
                setattr(__tmp3, field.name, getattr(other, field.name))
        __tmp3.on_fields_loaded()

    def on_fields_loaded(__tmp3) :
        pass

    @classmethod
    def from_json(
        __tmp5, gmi: "GMI", json_dict, *args: Any
    ) -> __typ0:
        # TODO Pull out args that are needed by constructor and use them here, removes a few pyre ignores
        obj = __tmp5(gmi, *args)

        for field in obj._fields:
            json_val = json_dict
            api_name = field.api_name
            if api_name is None:  # pragma: no cover
                raise ValueError("api_name should be known by this point")
            for val in api_name.split("."):
                json_val = json_val.get(val, None)
            setattr(obj, field.name, json_val)
        obj.on_fields_loaded()
        return obj


class RetrievableObject:
    def __tmp1(__tmp3) -> None:
        raise NotImplementedError  # pragma: no cover

    def __tmp0(__tmp3) :
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def get(gmi, *args) -> Type["RetrievableObject"]:
        raise NotImplementedError  # pragma: no cover
