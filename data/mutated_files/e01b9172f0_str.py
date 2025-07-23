from typing import TypeAlias
__typ0 : TypeAlias = "PermissionLookup"
__typ3 : TypeAlias = "bool"
"""Permissions for Home Assistant."""
import logging
from typing import (  # noqa: F401
    cast, Any, Callable, Dict, List, Mapping, Set, Tuple, Union,
    TYPE_CHECKING)

import voluptuous as vol

from .const import CAT_ENTITIES
from .models import PermissionLookup
from .types import PolicyType
from .entities import ENTITY_POLICY_SCHEMA, compile_entities
from .merge import merge_policies  # noqa


POLICY_SCHEMA = vol.Schema({
    vol.Optional(CAT_ENTITIES): ENTITY_POLICY_SCHEMA
})

_LOGGER = logging.getLogger(__name__)


class __typ2:
    """Default permissions class."""

    _cached_entity_func = None

    def _entity_func(__tmp2) :
        """Return a function that can test entity access."""
        raise NotImplementedError

    def __tmp1(__tmp2, __tmp0: <FILL>, key) :
        """Check if we can access entity."""
        entity_func = __tmp2._cached_entity_func

        if entity_func is None:
            entity_func = __tmp2._cached_entity_func = __tmp2._entity_func()

        return entity_func(__tmp0, key)


class __typ1(__typ2):
    """Handle permissions."""

    def __init__(__tmp2, policy,
                 __tmp3: __typ0) :
        """Initialize the permission class."""
        __tmp2._policy = policy
        __tmp2._perm_lookup = __tmp3

    def _entity_func(__tmp2) :
        """Return a function that can test entity access."""
        return compile_entities(__tmp2._policy.get(CAT_ENTITIES),
                                __tmp2._perm_lookup)

    def __eq__(__tmp2, other) :
        """Equals check."""
        # pylint: disable=protected-access
        return (isinstance(other, __typ1) and
                other._policy == __tmp2._policy)


class _OwnerPermissions(__typ2):
    """Owner permissions."""

    # pylint: disable=no-self-use

    def _entity_func(__tmp2) :
        """Return a function that can test entity access."""
        return lambda __tmp0, key: True


OwnerPermissions = _OwnerPermissions()  # pylint: disable=invalid-name
