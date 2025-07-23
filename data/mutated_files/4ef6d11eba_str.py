from typing import TypeAlias
__typ0 : TypeAlias = "ValueType"
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


def _entity_allowed(schema, __tmp5: str) \
        -> Union[__typ1, None]:
    """Test if an entity is allowed based on the keys."""
    if schema is None or isinstance(schema, __typ1):
        return schema
    assert isinstance(schema, dict)
    return schema.get(__tmp5)


def compile_entities(policy: CategoryType, __tmp1: PermissionLookup) \
        -> Callable[[str, str], __typ1]:
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not policy:
        def apply_policy_deny_all(__tmp3: str, __tmp5: str) :
            """Decline all."""
            return False

        return apply_policy_deny_all

    if policy is True:
        def apply_policy_allow_all(__tmp3: str, __tmp5: str) -> __typ1:
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
    if isinstance(entity_ids, __typ1):
        def __tmp2(__tmp3, __tmp5: str) :
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp2

    if entity_ids is not None:
        def allowed_entity_id_dict(__tmp3: str, __tmp5: str) \
                :
            """Test if allowed entity_id."""
            return _entity_allowed(
                entity_ids.get(__tmp3), __tmp5)  # type: ignore

        funcs.append(allowed_entity_id_dict)

    if isinstance(device_ids, __typ1):
        def allowed_device_id_bool(__tmp3, __tmp5) \
                -> Union[None, __typ1]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(allowed_device_id_bool)

    elif device_ids is not None:
        def allowed_device_id_dict(__tmp3: str, __tmp5: str) \
                -> Union[None, __typ1]:
            """Test if allowed device_id."""
            entity_entry = __tmp1.entity_registry.async_get(__tmp3)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return _entity_allowed(
                device_ids.get(entity_entry.device_id), __tmp5   # type: ignore
            )

        funcs.append(allowed_device_id_dict)

    if isinstance(domains, __typ1):
        def allowed_domain_bool(__tmp3: str, __tmp5) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(allowed_domain_bool)

    elif domains is not None:
        def __tmp4(__tmp3, __tmp5: str) \
                :
            """Test if allowed domain."""
            domain = __tmp3.split(".", 1)[0]
            return _entity_allowed(domains.get(domain), __tmp5)  # type: ignore

        funcs.append(__tmp4)

    if isinstance(all_entities, __typ1):
        def allowed_all_entities_bool(__tmp3, __tmp5: str) \
                :
            """Test if allowed domain."""
            return all_entities
        funcs.append(allowed_all_entities_bool)

    elif all_entities is not None:
        def allowed_all_entities_dict(__tmp3: str, __tmp5) \
                :
            """Test if allowed domain."""
            return _entity_allowed(all_entities, __tmp5)
        funcs.append(allowed_all_entities_dict)

    # Can happen if no valid subcategories specified
    if not funcs:
        def apply_policy_deny_all_2(__tmp3: str, __tmp5: str) :
            """Decline all."""
            return False

        return apply_policy_deny_all_2

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp0(__tmp3: <FILL>, __tmp5) :
            """Apply a single policy function."""
            return func(__tmp3, __tmp5) is True

        return __tmp0

    def apply_policy_funcs(__tmp3: str, __tmp5) -> __typ1:
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp3, __tmp5)
            if result is not None:
                return result
        return False

    return apply_policy_funcs
