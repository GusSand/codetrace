from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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


def _entity_allowed(__tmp1, __tmp12) \
        :
    """Test if an entity is allowed based on the keys."""
    if __tmp1 is None or isinstance(__tmp1, __typ0):
        return __tmp1
    assert isinstance(__tmp1, dict)
    return __tmp1.get(__tmp12)


def __tmp3(policy, __tmp5) \
        -> Callable[[str, str], __typ0]:
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not policy:
        def __tmp2(__tmp8: str, __tmp12: str) -> __typ0:
            """Decline all."""
            return False

        return __tmp2

    if policy is True:
        def apply_policy_allow_all(__tmp8, __tmp12: str) :
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
    if isinstance(entity_ids, __typ0):
        def __tmp6(__tmp8, __tmp12: str) -> __typ0:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp6

    if entity_ids is not None:
        def __tmp0(__tmp8: str, __tmp12) \
                -> Union[None, __typ0]:
            """Test if allowed entity_id."""
            return _entity_allowed(
                entity_ids.get(__tmp8), __tmp12)  # type: ignore

        funcs.append(__tmp0)

    if isinstance(device_ids, __typ0):
        def __tmp11(__tmp8: str, __tmp12: <FILL>) \
                -> Union[None, __typ0]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp11)

    elif device_ids is not None:
        def __tmp10(__tmp8: str, __tmp12: str) \
                :
            """Test if allowed device_id."""
            entity_entry = __tmp5.entity_registry.async_get(__tmp8)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return _entity_allowed(
                device_ids.get(entity_entry.device_id), __tmp12   # type: ignore
            )

        funcs.append(__tmp10)

    if isinstance(domains, __typ0):
        def __tmp9(__tmp8: str, __tmp12: str) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp9)

    elif domains is not None:
        def allowed_domain_dict(__tmp8: str, __tmp12) \
                :
            """Test if allowed domain."""
            domain = __tmp8.split(".", 1)[0]
            return _entity_allowed(domains.get(domain), __tmp12)  # type: ignore

        funcs.append(allowed_domain_dict)

    if isinstance(all_entities, __typ0):
        def __tmp7(__tmp8, __tmp12: str) \
                -> Union[None, __typ0]:
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp7)

    elif all_entities is not None:
        def allowed_all_entities_dict(__tmp8: str, __tmp12) \
                -> Union[None, __typ0]:
            """Test if allowed domain."""
            return _entity_allowed(all_entities, __tmp12)
        funcs.append(allowed_all_entities_dict)

    # Can happen if no valid subcategories specified
    if not funcs:
        def apply_policy_deny_all_2(__tmp8, __tmp12) -> __typ0:
            """Decline all."""
            return False

        return apply_policy_deny_all_2

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp4(__tmp8: str, __tmp12) :
            """Apply a single policy function."""
            return func(__tmp8, __tmp12) is True

        return __tmp4

    def apply_policy_funcs(__tmp8: str, __tmp12) :
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp8, __tmp12)
            if result is not None:
                return result
        return False

    return apply_policy_funcs
