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


def _entity_allowed(schema, __tmp11) \
        :
    """Test if an entity is allowed based on the keys."""
    if schema is None or isinstance(schema, __typ0):
        return schema
    assert isinstance(schema, dict)
    return schema.get(__tmp11)


def __tmp3(__tmp8, __tmp4: PermissionLookup) \
        -> Callable[[str, str], __typ0]:
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp8:
        def apply_policy_deny_all(__tmp6: str, __tmp11) -> __typ0:
            """Decline all."""
            return False

        return apply_policy_deny_all

    if __tmp8 is True:
        def apply_policy_allow_all(__tmp6, __tmp11: str) :
            """Approve all."""
            return True

        return apply_policy_allow_all

    assert isinstance(__tmp8, dict)

    domains = __tmp8.get(ENTITY_DOMAINS)
    device_ids = __tmp8.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp8.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp8.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, __typ0):
        def allowed_entity_id_bool(__tmp6, __tmp11: str) -> __typ0:
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return allowed_entity_id_bool

    if entity_ids is not None:
        def __tmp0(__tmp6, __tmp11) \
                :
            """Test if allowed entity_id."""
            return _entity_allowed(
                entity_ids.get(__tmp6), __tmp11)  # type: ignore

        funcs.append(__tmp0)

    if isinstance(device_ids, __typ0):
        def __tmp2(__tmp6, __tmp11) \
                :
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp2)

    elif device_ids is not None:
        def allowed_device_id_dict(__tmp6: str, __tmp11) \
                -> Union[None, __typ0]:
            """Test if allowed device_id."""
            entity_entry = __tmp4.entity_registry.async_get(__tmp6)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return _entity_allowed(
                device_ids.get(entity_entry.device_id), __tmp11   # type: ignore
            )

        funcs.append(allowed_device_id_dict)

    if isinstance(domains, __typ0):
        def __tmp9(__tmp6: str, __tmp11) \
                :
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp9)

    elif domains is not None:
        def __tmp7(__tmp6: <FILL>, __tmp11: str) \
                :
            """Test if allowed domain."""
            domain = __tmp6.split(".", 1)[0]
            return _entity_allowed(domains.get(domain), __tmp11)  # type: ignore

        funcs.append(__tmp7)

    if isinstance(all_entities, __typ0):
        def __tmp5(__tmp6, __tmp11) \
                :
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp5)

    elif all_entities is not None:
        def __tmp1(__tmp6, __tmp11: str) \
                :
            """Test if allowed domain."""
            return _entity_allowed(all_entities, __tmp11)
        funcs.append(__tmp1)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp10(__tmp6, __tmp11) :
            """Decline all."""
            return False

        return __tmp10

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def apply_policy_func(__tmp6, __tmp11: str) -> __typ0:
            """Apply a single policy function."""
            return func(__tmp6, __tmp11) is True

        return apply_policy_func

    def apply_policy_funcs(__tmp6, __tmp11) -> __typ0:
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp6, __tmp11)
            if result is not None:
                return result
        return False

    return apply_policy_funcs
