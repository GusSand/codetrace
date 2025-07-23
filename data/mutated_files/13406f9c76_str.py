from typing import TypeAlias
__typ2 : TypeAlias = "T"
__typ1 : TypeAlias = "JsonType"
# pyre-strict
from typing import Dict, TYPE_CHECKING, Type, List, Tuple, Optional, TypeVar, Any

from lowerpines.endpoints.request import JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI

__typ2 = TypeVar("T")


class __typ0:
    def __tmp1(self) :
        self.name = ""
        self.api_name: Optional[str] = None

    def with_api_name(self, api_name) -> "Field":
        self.api_name = api_name
        return self

    def with_type(self, _) -> __typ2:
        # This is intentional, it allows us to trick type-checkers into asserting that the field type is T,
        # which will be true at runtime, since Field types are erased by the metaclass
        return self  # type: ignore

    def with_field_name(self, name) :
        self.name = name
        if self.api_name is None:
            self.api_name = name
        return self


class AbstractObjectType(type):
    def __new__(
        mcs,
        name: <FILL>,
        bases: Tuple[Type["AbstractObjectType"]],
        __tmp0,
    ) -> "AbstractObjectType":
        new_attrs = {}  # type: ignore
        fields = []
        for attr_name, attr_value in __tmp0.items():
            if type(attr_value) == __typ0:
                attr_value.with_field_name(attr_name)
                fields.append(attr_value)
                new_attrs[attr_name] = None
            else:
                new_attrs[attr_name] = attr_value
        new_attrs["_fields"] = fields  # type: ignore

        return super(AbstractObjectType, mcs).__new__(  # type: ignore
            mcs, name, bases, new_attrs
        )


__typ4 = TypeVar("TAbstractObject", bound="AbstractObject")


class __typ3(metaclass=AbstractObjectType):
    _fields: List[__typ0] = []

    def __tmp1(self, _: "GMI", *_args) :
        pass

    def _refresh_from_other(self, other: __typ4) -> None:
        if other is not None:
            for field in self._fields:
                setattr(self, field.name, getattr(other, field.name))
        self.on_fields_loaded()

    def on_fields_loaded(self) :
        pass

    @classmethod
    def from_json(
        cls, gmi, json_dict, *args: Any
    ) :
        # TODO Pull out args that are needed by constructor and use them here, removes a few pyre ignores
        obj = cls(gmi, *args)

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
    def save(self) :
        raise NotImplementedError  # pragma: no cover

    def refresh(self) -> None:
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def get(gmi, *args) :
        raise NotImplementedError  # pragma: no cover
