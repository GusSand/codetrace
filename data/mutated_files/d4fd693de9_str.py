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


def __tmp13(__tmp15: ValueType, __tmp2) \
        :
    """Test if an entity is allowed based on the keys."""
    if __tmp15 is None or isinstance(__tmp15, bool):
        return __tmp15
    assert isinstance(__tmp15, dict)
    return __tmp15.get(__tmp2)


def __tmp8(__tmp5: CategoryType, __tmp18: PermissionLookup) \
        :
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp5:
        def __tmp16(__tmp4, __tmp2: str) :
            """Decline all."""
            return False

        return __tmp16

    if __tmp5 is True:
        def __tmp7(__tmp4, __tmp2) :
            """Approve all."""
            return True

        return __tmp7

    assert isinstance(__tmp5, dict)

    domains = __tmp5.get(ENTITY_DOMAINS)
    device_ids = __tmp5.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp5.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp5.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, bool):
        def __tmp9(__tmp4, __tmp2) -> bool:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp9

    if entity_ids is not None:
        def __tmp14(__tmp4, __tmp2: str) \
                :
            """Test if allowed entity_id."""
            return __tmp13(
                entity_ids.get(__tmp4), __tmp2)  # type: ignore

        funcs.append(__tmp14)

    if isinstance(device_ids, bool):
        def __tmp1(__tmp4, __tmp2) \
                -> Union[None, bool]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp1)

    elif device_ids is not None:
        def __tmp0(__tmp4, __tmp2) \
                :
            """Test if allowed device_id."""
            entity_entry = __tmp18.entity_registry.async_get(__tmp4)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return __tmp13(
                device_ids.get(entity_entry.device_id), __tmp2   # type: ignore
            )

        funcs.append(__tmp0)

    if isinstance(domains, bool):
        def __tmp11(__tmp4, __tmp2: str) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp11)

    elif domains is not None:
        def __tmp6(__tmp4, __tmp2) \
                :
            """Test if allowed domain."""
            domain = __tmp4.split(".", 1)[0]
            return __tmp13(domains.get(domain), __tmp2)  # type: ignore

        funcs.append(__tmp6)

    if isinstance(all_entities, bool):
        def __tmp3(__tmp4: str, __tmp2) \
                :
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp3)

    elif all_entities is not None:
        def __tmp17(__tmp4: str, __tmp2) \
                :
            """Test if allowed domain."""
            return __tmp13(all_entities, __tmp2)
        funcs.append(__tmp17)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp12(__tmp4, __tmp2) :
            """Decline all."""
            return False

        return __tmp12

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def apply_policy_func(__tmp4: str, __tmp2: <FILL>) :
            """Apply a single policy function."""
            return func(__tmp4, __tmp2) is True

        return apply_policy_func

    def __tmp10(__tmp4: str, __tmp2) :
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp4, __tmp2)
            if result is not None:
                return result
        return False

    return __tmp10
