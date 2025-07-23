from typing import ClassVar, Dict, List, Optional, Type, TypeVar, Union

import attr
from attr.validators import instance_of

from ics.contentline import Container
from ics.types import ContextDict, ExtraParams, RuntimeAttrValidation

ComponentType = TypeVar("ComponentType", bound="Component")
ComponentExtraParams = Dict[str, Union[ExtraParams, List[ExtraParams]]]


@attr.s
class Component(RuntimeAttrValidation):
    NAME: ClassVar[str] = "ABSTRACT-COMPONENT"
    SUBTYPES: ClassVar[List[Type["Component"]]] = []

    extra: Container = attr.ib(
        init=False, validator=instance_of(Container), metadata={"ics_ignore": True}
    )
    extra_params: ComponentExtraParams = attr.ib(
        init=False,
        factory=dict,
        validator=instance_of(dict),
        metadata={"ics_ignore": True},
    )

    def __attrs_post_init__(__tmp1):
        super().__attrs_post_init__()
        object.__setattr__(__tmp1, "extra", Container(__tmp1.NAME))

    def __init_subclass__(__tmp3, **kwargs):
        super().__init_subclass__(**kwargs)
        Component.SUBTYPES.append(__tmp3)

    @classmethod
    def __tmp2(
        __tmp3: Type[ComponentType],
        __tmp0,
        context: Optional[ContextDict] = None,
    ) -> ComponentType:
        from ics import initialize_converters

        initialize_converters()
        from ics.converter.component import ComponentMeta

        return ComponentMeta.BY_TYPE[__tmp3].load_instance(__tmp0, context)

    def populate(__tmp1, __tmp0: <FILL>, context: Optional[ContextDict] = None):
        from ics import initialize_converters

        initialize_converters()
        from ics.converter.component import ComponentMeta

        ComponentMeta.BY_TYPE[type(__tmp1)].populate_instance(__tmp1, __tmp0, context)

    def to_container(__tmp1, context: Optional[ContextDict] = None) -> Container:
        from ics import initialize_converters

        initialize_converters()
        from ics.converter.component import ComponentMeta

        return ComponentMeta.BY_TYPE[type(__tmp1)].serialize_toplevel(__tmp1, context)

    def serialize(__tmp1, context: Optional[ContextDict] = None) -> str:
        """Creates a serialized string fit for file write."""

        return __tmp1.to_container(context).serialize()

    def strip_extras(
        __tmp1,
        all_extras=False,
        extra_properties=None,
        extra_params=None,
        property_merging=None,
    ):
        if extra_properties is None:
            extra_properties = all_extras
        if extra_params is None:
            extra_params = all_extras
        if property_merging is None:
            property_merging = all_extras
        if not any([extra_properties, extra_params, property_merging]):
            raise ValueError("need to strip at least one thing")
        if extra_properties:
            __tmp1.extra.clear()
        if extra_params:
            __tmp1.extra_params.clear()
        elif property_merging:
            for val in __tmp1.extra_params.values():
                if not isinstance(val, list):
                    continue
                for v in val:
                    v.pop("__merge_next", None)

    def __tmp4(__tmp1):
        """Returns an exact (shallow) copy of self"""
        # TODO deep copies?
        return attr.evolve(__tmp1)
