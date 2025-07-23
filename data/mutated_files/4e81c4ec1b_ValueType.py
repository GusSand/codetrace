from typing import TypeAlias
__typ0 : TypeAlias = "str"
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
    __typ0: SINGLE_ENTITY_SCHEMA
}))

ENTITY_POLICY_SCHEMA = vol.Any(True, vol.Schema({
    vol.Optional(SUBCAT_ALL): SINGLE_ENTITY_SCHEMA,
    vol.Optional(ENTITY_DEVICE_IDS): ENTITY_VALUES_SCHEMA,
    vol.Optional(ENTITY_DOMAINS): ENTITY_VALUES_SCHEMA,
    vol.Optional(ENTITY_ENTITY_IDS): ENTITY_VALUES_SCHEMA,
}))


def __tmp14(__tmp16: <FILL>, __tmp2) \
        :
    """Test if an entity is allowed based on the keys."""
    if __tmp16 is None or isinstance(__tmp16, bool):
        return __tmp16
    assert isinstance(__tmp16, dict)
    return __tmp16.get(__tmp2)


def __tmp9(__tmp7: CategoryType, __tmp19: PermissionLookup) \
        :
    """Compile policy into a function that tests policy."""
    # None, Empty Dict, False
    if not __tmp7:
        def __tmp18(__tmp5: __typ0, __tmp2: __typ0) -> bool:
            """Decline all."""
            return False

        return __tmp18

    if __tmp7 is True:
        def __tmp8(__tmp5: __typ0, __tmp2: __typ0) -> bool:
            """Approve all."""
            return True

        return __tmp8

    assert isinstance(__tmp7, dict)

    domains = __tmp7.get(ENTITY_DOMAINS)
    device_ids = __tmp7.get(ENTITY_DEVICE_IDS)
    entity_ids = __tmp7.get(ENTITY_ENTITY_IDS)
    all_entities = __tmp7.get(SUBCAT_ALL)

    funcs = []  # type: List[Callable[[str, str], Union[None, bool]]]

    # The order of these functions matter. The more precise are at the top.
    # If a function returns None, they cannot handle it.
    # If a function returns a boolean, that's the result to return.

    # Setting entity_ids to a boolean is final decision for permissions
    # So return right away.
    if isinstance(entity_ids, bool):
        def __tmp10(__tmp5: __typ0, __tmp2: __typ0) :
            """Test if allowed entity_id."""
            return entity_ids  # type: ignore

        return __tmp10

    if entity_ids is not None:
        def __tmp15(__tmp5, __tmp2: __typ0) \
                -> Union[None, bool]:
            """Test if allowed entity_id."""
            return __tmp14(
                entity_ids.get(__tmp5), __tmp2)  # type: ignore

        funcs.append(__tmp15)

    if isinstance(device_ids, bool):
        def __tmp1(__tmp5: __typ0, __tmp2: __typ0) \
                -> Union[None, bool]:
            """Test if allowed device_id."""
            return device_ids

        funcs.append(__tmp1)

    elif device_ids is not None:
        def __tmp0(__tmp5: __typ0, __tmp2: __typ0) \
                -> Union[None, bool]:
            """Test if allowed device_id."""
            entity_entry = __tmp19.entity_registry.async_get(__tmp5)

            if entity_entry is None or entity_entry.device_id is None:
                return None

            return __tmp14(
                device_ids.get(entity_entry.device_id), __tmp2   # type: ignore
            )

        funcs.append(__tmp0)

    if isinstance(domains, bool):
        def __tmp12(__tmp5, __tmp2: __typ0) \
                -> Union[None, bool]:
            """Test if allowed domain."""
            return domains

        funcs.append(__tmp12)

    elif domains is not None:
        def __tmp6(__tmp5: __typ0, __tmp2: __typ0) \
                -> Union[None, bool]:
            """Test if allowed domain."""
            domain = __tmp5.split(".", 1)[0]
            return __tmp14(domains.get(domain), __tmp2)  # type: ignore

        funcs.append(__tmp6)

    if isinstance(all_entities, bool):
        def __tmp4(__tmp5: __typ0, __tmp2: __typ0) \
                :
            """Test if allowed domain."""
            return all_entities
        funcs.append(__tmp4)

    elif all_entities is not None:
        def __tmp17(__tmp5: __typ0, __tmp2: __typ0) \
                -> Union[None, bool]:
            """Test if allowed domain."""
            return __tmp14(all_entities, __tmp2)
        funcs.append(__tmp17)

    # Can happen if no valid subcategories specified
    if not funcs:
        def __tmp13(__tmp5: __typ0, __tmp2: __typ0) -> bool:
            """Decline all."""
            return False

        return __tmp13

    if len(funcs) == 1:
        func = funcs[0]

        @wraps(func)
        def __tmp3(__tmp5: __typ0, __tmp2: __typ0) :
            """Apply a single policy function."""
            return func(__tmp5, __tmp2) is True

        return __tmp3

    def __tmp11(__tmp5: __typ0, __tmp2: __typ0) -> bool:
        """Apply several policy functions."""
        for func in funcs:
            result = func(__tmp5, __tmp2)
            if result is not None:
                return result
        return False

    return __tmp11
