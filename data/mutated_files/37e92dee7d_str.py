from typing import TypeAlias
__typ1 : TypeAlias = "ValueType"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "PermissionLookup"
"""Entity permissions."""
from functools import wraps
from typing import Callable, List, Union  # noqa: F401

import voluptuous as vol

from .const import SUBCAT_ALL, POLICY_READ, POLICY_CONTROL, POLICY_EDIT
from .models import PermissionLookup
from .types import CategoryType, ValueType

SINGLE_ENTITY_SCHEMA = vol.Any(True, vol.Schema({
    vol.Optional(POLICY_READ): True,
    vol.Optional(POLICY_CONTROL): True,
    vol.Optional(POLICY_EDIT): True,
}))

ENTITY_DOMAINS = 'domains'
ENTITY_DEVICE_IDS = 'device_ids'
ENTITY_ENTITY_IDS = 'entity_ids'

ENTITY_VALUES_SCHEMA = vol.Any(True, vol.Schema({
    str: SINGLE_ENTITY_SCHEMA
}))

ENTITY_POLICY_SCHEMA = vol.Any(True, vol.Schema({
    vol.Optional(SUBCAT_ALL): SINGLE_ENTITY_SCHEMA,
    vol.Optional(ENTITY_DEVICE_IDS): ENTITY_VALUES_SCHEMA,
    vol.Optional(ENTITY_DOMAINS): ENTITY_VALUES_SCHEMA,
    vol.Optional(ENTITY_ENTITY_IDS): ENTITY_VALUES_SCHEMA,
}))


def __tmp15(schema: __typ1, __tmp14) \
        :
    """Test if an entity is allowed based on the keys."""
    if schema is None or isinstance(schema, __typ2):
        return schema
    assert isinstance(schema, dict)
    return schema.get(__tmp14)


def compile_entities(__tmp9: CategoryType, __tmp4: __typ0) \
        -> Callable[[str, str], __typ2]:
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp9:
        def __tmp2(__tmp8: str, __tmp14: str) -> __typ2:
            """Decline all."""
            return False

        return __tmp2

    if __tmp9 is True:
        def apply_policy_allow_all(__tmp8: str, __tmp14: str) -> __typ2:
            """Approve all."""
            return True

        return apply_policy_allow_all

    assert isinstance(__tmp9, dict)

    domains = __tmp9.get(ENTITY_DOMAINS)
    device_ids = __tmp9.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp9.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp9.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, __typ2):
        def __tmp5(__tmp8: str, __tmp14: str) -> __typ2:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp5

    if entity_ids is not None:
        def __tmp0(__tmp8, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed entity_id."""
            return __tmp15(
                entity_ids.get(__tmp8), __tmp14)  # type: ignore

        funcs.append(__tmp0)

    if isinstance(device_ids, __typ2):
        def __tmp13(__tmp8: <FILL>, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp13)

    elif device_ids is not None:
        def allowed_device_id_dict(__tmp8: str, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed device_id."""
            entity_entry = __tmp4.entity_registry.async_get(__tmp8)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return __tmp15(
                device_ids.get(entity_entry.device_id), __tmp14   # type: ignore
            )

        funcs.append(allowed_device_id_dict)

    if isinstance(domains, __typ2):
        def __tmp12(__tmp8: str, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp12)

    elif domains is not None:
        def __tmp11(__tmp8: str, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed domain."""
            domain = __tmp8.split(".", 1)[0]
            return __tmp15(domains.get(domain), __tmp14)  # type: ignore

        funcs.append(__tmp11)

    if isinstance(all_entities, __typ2):
        def __tmp7(__tmp8: str, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp7)

    elif all_entities is not None:
        def __tmp1(__tmp8: str, __tmp14: str) \
                -> Union[None, __typ2]:
            """Test if allowed domain."""
            return __tmp15(all_entities, __tmp14)
        funcs.append(__tmp1)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp6(__tmp8: str, __tmp14: str) -> __typ2:
            """Decline all."""
            return False

        return __tmp6

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp3(__tmp8: str, __tmp14: str) :
            """Apply a single policy function."""
            return func(__tmp8, __tmp14) is True

        return __tmp3

    def __tmp10(__tmp8, __tmp14: str) -> __typ2:
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp8, __tmp14)
            if result is not None:
                return result
        return False

    return __tmp10
