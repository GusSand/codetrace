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


def _entity_allowed(schema, key: <FILL>) \
        -> Union[__typ3, None]:
    """Test if an entity is allowed based on the keys."""
    if schema is None or isinstance(schema, __typ3):
        return schema
    assert isinstance(schema, dict)
    return schema.get(key)


def __tmp0(policy: __typ2, perm_lookup: __typ0) \
        :
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not policy:
        def apply_policy_deny_all(__tmp2: str, key) -> __typ3:
            """Decline all."""
            return False

        return apply_policy_deny_all

    if policy is True:
        def apply_policy_allow_all(__tmp2: str, key) :
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
        def allowed_entity_id_bool(__tmp2: str, key: str) -> __typ3:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return allowed_entity_id_bool

    if entity_ids is not None:
        def allowed_entity_id_dict(__tmp2: str, key: str) \
                :
            """Test if allowed entity_id."""
            return _entity_allowed(
                entity_ids.get(__tmp2), key)  # type: ignore

        funcs.append(allowed_entity_id_dict)

    if isinstance(device_ids, __typ3):
        def allowed_device_id_bool(__tmp2: str, key: str) \
                :
            """Test if allowed device_id."""
            return device_ids

        funcs.append(allowed_device_id_bool)

    elif device_ids is not None:
        def __tmp3(__tmp2: str, key: str) \
                -> Union[None, __typ3]:
            """Test if allowed device_id."""
            entity_entry = perm_lookup.entity_registry.async_get(__tmp2)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return _entity_allowed(
                device_ids.get(entity_entry.device_id), key   # type: ignore
            )

        funcs.append(__tmp3)

    if isinstance(domains, __typ3):
        def allowed_domain_bool(__tmp2: str, key: str) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(allowed_domain_bool)

    elif domains is not None:
        def allowed_domain_dict(__tmp2, key) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            domain = __tmp2.split(".", 1)[0]
            return _entity_allowed(domains.get(domain), key)  # type: ignore

        funcs.append(allowed_domain_dict)

    if isinstance(all_entities, __typ3):
        def __tmp1(__tmp2, key: str) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp1)

    elif all_entities is not None:
        def allowed_all_entities_dict(__tmp2, key) \
                -> Union[None, __typ3]:
            """Test if allowed domain."""
            return _entity_allowed(all_entities, key)
        funcs.append(allowed_all_entities_dict)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp4(__tmp2, key: str) :
            """Decline all."""
            return False

        return __tmp4

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def apply_policy_func(__tmp2: str, key: str) -> __typ3:
            """Apply a single policy function."""
            return func(__tmp2, key) is True

        return apply_policy_func

    def apply_policy_funcs(__tmp2: str, key) :
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp2, key)
            if result is not None:
                return result
        return False

    return apply_policy_funcs
