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


def _entity_allowed(__tmp1, __tmp15: str) \
        :
    """Test if an entity is allowed based on the keys."""
    if __tmp1 is None or isinstance(__tmp1, __typ1):
        return __tmp1
    assert isinstance(__tmp1, dict)
    return __tmp1.get(__tmp15)


def __tmp6(__tmp11, __tmp5) \
        -> Callable[[str, str], __typ1]:
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp11:
        def __tmp4(__tmp10: str, __tmp15: str) -> __typ1:
            """Decline all."""
            return False

        return __tmp4

    if __tmp11 is True:
        def __tmp3(__tmp10: str, __tmp15) :
            """Approve all."""
            return True

        return __tmp3

    assert isinstance(__tmp11, dict)

    domains = __tmp11.get(ENTITY_DOMAINS)
    device_ids = __tmp11.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp11.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp11.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, __typ1):
        def __tmp8(__tmp10: str, __tmp15: str) -> __typ1:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp8

    if entity_ids is not None:
        def __tmp0(__tmp10, __tmp15) \
                -> Union[None, __typ1]:
            """Test if allowed entity_id."""
            return _entity_allowed(
                entity_ids.get(__tmp10), __tmp15)  # type: ignore

        funcs.append(__tmp0)

    if isinstance(device_ids, __typ1):
        def __tmp7(__tmp10, __tmp15) \
                :
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp7)

    elif device_ids is not None:
        def __tmp13(__tmp10, __tmp15) \
                :
            """Test if allowed device_id."""
            entity_entry = __tmp5.entity_registry.async_get(__tmp10)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return _entity_allowed(
                device_ids.get(entity_entry.device_id), __tmp15   # type: ignore
            )

        funcs.append(__tmp13)

    if isinstance(domains, __typ1):
        def __tmp12(__tmp10, __tmp15) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp12)

    elif domains is not None:
        def allowed_domain_dict(__tmp10, __tmp15: str) \
                -> Union[None, __typ1]:
            """Test if allowed domain."""
            domain = __tmp10.split(".", 1)[0]
            return _entity_allowed(domains.get(domain), __tmp15)  # type: ignore

        funcs.append(allowed_domain_dict)

    if isinstance(all_entities, __typ1):
        def __tmp9(__tmp10: str, __tmp15: <FILL>) \
                -> Union[None, __typ1]:
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp9)

    elif all_entities is not None:
        def __tmp2(__tmp10, __tmp15: str) \
                :
            """Test if allowed domain."""
            return _entity_allowed(all_entities, __tmp15)
        funcs.append(__tmp2)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp14(__tmp10, __tmp15) -> __typ1:
            """Decline all."""
            return False

        return __tmp14

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def apply_policy_func(__tmp10: str, __tmp15) -> __typ1:
            """Apply a single policy function."""
            return func(__tmp10, __tmp15) is True

        return apply_policy_func

    def apply_policy_funcs(__tmp10: str, __tmp15: str) :
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp10, __tmp15)
            if result is not None:
                return result
        return False

    return apply_policy_funcs
