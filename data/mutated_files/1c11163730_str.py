from typing import TypeAlias
__typ1 : TypeAlias = "ValueType"
__typ0 : TypeAlias = "PermissionLookup"
__typ2 : TypeAlias = "CategoryType"
__typ3 : TypeAlias = "bool"
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


def __tmp17(__tmp1, __tmp16: str) \
        :
    """Test if an entity is allowed based on the keys."""
    if __tmp1 is None or isinstance(__tmp1, __typ3):
        return __tmp1
    assert isinstance(__tmp1, dict)
    return __tmp1.get(__tmp16)


def __tmp4(__tmp12: __typ2, __tmp6) \
        :
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp12:
        def __tmp3(__tmp11, __tmp16: str) :
            """Decline all."""
            return False

        return __tmp3

    if __tmp12 is True:
        def __tmp2(__tmp11: str, __tmp16: str) :
            """Approve all."""
            return True

        return __tmp2

    assert isinstance(__tmp12, dict)

    domains = __tmp12.get(ENTITY_DOMAINS)
    device_ids = __tmp12.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp12.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp12.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, __typ3):
        def __tmp8(__tmp11, __tmp16: str) -> __typ3:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp8

    if entity_ids is not None:
        def __tmp0(__tmp11, __tmp16) \
                :
            """Test if allowed entity_id."""
            return __tmp17(
                entity_ids.get(__tmp11), __tmp16)  # type: ignore

        funcs.append(__tmp0)

    if isinstance(device_ids, __typ3):
        def allowed_device_id_bool(__tmp11, __tmp16: str) \
                -> Union[None, __typ3]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(allowed_device_id_bool)

    elif device_ids is not None:
        def allowed_device_id_dict(__tmp11, __tmp16: str) \
                :
            """Test if allowed device_id."""
            entity_entry = __tmp6.entity_registry.async_get(__tmp11)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return __tmp17(
                device_ids.get(entity_entry.device_id), __tmp16   # type: ignore
            )

        funcs.append(allowed_device_id_dict)

    if isinstance(domains, __typ3):
        def __tmp14(__tmp11, __tmp16) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp14)

    elif domains is not None:
        def __tmp10(__tmp11, __tmp16) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            domain = __tmp11.split(".", 1)[0]
            return __tmp17(domains.get(domain), __tmp16)  # type: ignore

        funcs.append(__tmp10)

    if isinstance(all_entities, __typ3):
        def __tmp9(__tmp11: <FILL>, __tmp16) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp9)

    elif all_entities is not None:
        def __tmp7(__tmp11, __tmp16) \
                :
            """Test if allowed domain."""
            return __tmp17(all_entities, __tmp16)
        funcs.append(__tmp7)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp15(__tmp11, __tmp16: str) -> __typ3:
            """Decline all."""
            return False

        return __tmp15

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp5(__tmp11, __tmp16) :
            """Apply a single policy function."""
            return func(__tmp11, __tmp16) is True

        return __tmp5

    def __tmp13(__tmp11, __tmp16) :
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp11, __tmp16)
            if result is not None:
                return result
        return False

    return __tmp13
