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


def __tmp11(__tmp1: __typ1, __tmp10: str) \
        :
    """Test if an entity is allowed based on the keys."""
    if __tmp1 is None or isinstance(__tmp1, __typ3):
        return __tmp1
    assert isinstance(__tmp1, dict)
    return __tmp1.get(__tmp10)


def compile_entities(policy, __tmp3) \
        :
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not policy:
        def __tmp0(__tmp6: str, __tmp10: str) -> __typ3:
            """Decline all."""
            return False

        return __tmp0

    if policy is True:
        def apply_policy_allow_all(__tmp6, __tmp10) -> __typ3:
            """Approve all."""
            return True

        return apply_policy_allow_all

    assert isinstance(policy, dict)

    domains = policy.get(ENTITY_DOMAINS)
    device_ids = policy.get(ENTITY_DEVICE_IDS)
    entity_ids = policy.get(ENTITY_ENTITY_IDS)
    all_entities = policy.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, __typ3):
        def __tmp4(__tmp6: str, __tmp10) :
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp4

    if entity_ids is not None:
        def allowed_entity_id_dict(__tmp6, __tmp10) \
                -> Union[None, __typ3]:
            """Test if allowed entity_id."""
            return __tmp11(
                entity_ids.get(__tmp6), __tmp10)  # type: ignore

        funcs.append(allowed_entity_id_dict)

    if isinstance(device_ids, __typ3):
        def __tmp9(__tmp6: str, __tmp10) \
                -> Union[None, __typ3]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp9)

    elif device_ids is not None:
        def allowed_device_id_dict(__tmp6, __tmp10: str) \
                :
            """Test if allowed device_id."""
            entity_entry = __tmp3.entity_registry.async_get(__tmp6)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return __tmp11(
                device_ids.get(entity_entry.device_id), __tmp10   # type: ignore
            )

        funcs.append(allowed_device_id_dict)

    if isinstance(domains, __typ3):
        def allowed_domain_bool(__tmp6: <FILL>, __tmp10: str) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(allowed_domain_bool)

    elif domains is not None:
        def __tmp7(__tmp6, __tmp10: str) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            domain = __tmp6.split(".", 1)[0]
            return __tmp11(domains.get(domain), __tmp10)  # type: ignore

        funcs.append(__tmp7)

    if isinstance(all_entities, __typ3):
        def allowed_all_entities_bool(__tmp6: str, __tmp10: str) \
                :
            """Test if allowed domain."""
            return all_entities
        funcs.append(allowed_all_entities_bool)

    elif all_entities is not None:
        def allowed_all_entities_dict(__tmp6: str, __tmp10) \
                :
            """Test if allowed domain."""
            return __tmp11(all_entities, __tmp10)
        funcs.append(allowed_all_entities_dict)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp5(__tmp6: str, __tmp10: str) :
            """Decline all."""
            return False

        return __tmp5

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp2(__tmp6: str, __tmp10) :
            """Apply a single policy function."""
            return func(__tmp6, __tmp10) is True

        return __tmp2

    def __tmp8(__tmp6, __tmp10: str) -> __typ3:
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp6, __tmp10)
            if result is not None:
                return result
        return False

    return __tmp8
