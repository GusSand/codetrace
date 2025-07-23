from typing import TypeAlias
__typ0 : TypeAlias = "CategoryType"
__typ1 : TypeAlias = "bool"
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


def __tmp16(__tmp0, __tmp15: str) \
        -> Union[__typ1, None]:
    """Test if an entity is allowed based on the keys."""
    if __tmp0 is None or isinstance(__tmp0, __typ1):
        return __tmp0
    assert isinstance(__tmp0, dict)
    return __tmp0.get(__tmp15)


def __tmp3(__tmp10, __tmp4: PermissionLookup) \
        :
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp10:
        def apply_policy_deny_all(__tmp9, __tmp15: str) -> __typ1:
            """Decline all."""
            return False

        return apply_policy_deny_all

    if __tmp10 is True:
        def __tmp2(__tmp9: <FILL>, __tmp15: str) -> __typ1:
            """Approve all."""
            return True

        return __tmp2

    assert isinstance(__tmp10, dict)

    domains = __tmp10.get(ENTITY_DOMAINS)
    device_ids = __tmp10.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp10.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp10.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, __typ1):
        def __tmp6(__tmp9, __tmp15: str) -> __typ1:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp6

    if entity_ids is not None:
        def allowed_entity_id_dict(__tmp9, __tmp15: str) \
                :
            """Test if allowed entity_id."""
            return __tmp16(
                entity_ids.get(__tmp9), __tmp15)  # type: ignore

        funcs.append(allowed_entity_id_dict)

    if isinstance(device_ids, __typ1):
        def __tmp14(__tmp9: str, __tmp15: str) \
                :
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp14)

    elif device_ids is not None:
        def __tmp13(__tmp9, __tmp15: str) \
                -> Union[None, __typ1]:
            """Test if allowed device_id."""
            entity_entry = __tmp4.entity_registry.async_get(__tmp9)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return __tmp16(
                device_ids.get(entity_entry.device_id), __tmp15   # type: ignore
            )

        funcs.append(__tmp13)

    if isinstance(domains, __typ1):
        def __tmp12(__tmp9: str, __tmp15) \
                -> Union[None, __typ1]:
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp12)

    elif domains is not None:
        def __tmp11(__tmp9, __tmp15: str) \
                :
            """Test if allowed domain."""
            domain = __tmp9.split(".", 1)[0]
            return __tmp16(domains.get(domain), __tmp15)  # type: ignore

        funcs.append(__tmp11)

    if isinstance(all_entities, __typ1):
        def __tmp8(__tmp9: str, __tmp15: str) \
                :
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp8)

    elif all_entities is not None:
        def __tmp1(__tmp9: str, __tmp15) \
                -> Union[None, __typ1]:
            """Test if allowed domain."""
            return __tmp16(all_entities, __tmp15)
        funcs.append(__tmp1)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp7(__tmp9: str, __tmp15) -> __typ1:
            """Decline all."""
            return False

        return __tmp7

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp5(__tmp9: str, __tmp15: str) -> __typ1:
            """Apply a single policy function."""
            return func(__tmp9, __tmp15) is True

        return __tmp5

    def apply_policy_funcs(__tmp9: str, __tmp15: str) -> __typ1:
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp9, __tmp15)
            if result is not None:
                return result
        return False

    return apply_policy_funcs
