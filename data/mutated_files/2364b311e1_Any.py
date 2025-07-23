from typing import TypeAlias
__typ1 : TypeAlias = "bool"
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


class AbstractPermissions:
    """Default permissions class."""

    _cached_entity_func = None

    def _entity_func(__tmp0) :
        """Return a function that can test entity access."""
        raise NotImplementedError

    def __tmp2(__tmp0, __tmp3: str, key: str) :
        """Check if we can access entity."""
        entity_func = __tmp0._cached_entity_func

        if entity_func is None:
            entity_func = __tmp0._cached_entity_func = __tmp0._entity_func()

        return entity_func(__tmp3, key)


class PolicyPermissions(AbstractPermissions):
    """Handle permissions."""

    def __tmp4(__tmp0, policy: PolicyType,
                 perm_lookup: PermissionLookup) -> None:
        """Initialize the permission class."""
        __tmp0._policy = policy
        __tmp0._perm_lookup = perm_lookup

    def _entity_func(__tmp0) -> Callable[[str, str], __typ1]:
        """Return a function that can test entity access."""
        return compile_entities(__tmp0._policy.get(CAT_ENTITIES),
                                __tmp0._perm_lookup)

    def __tmp1(__tmp0, other: <FILL>) :
        """Equals check."""
        # pylint: disable=protected-access
        return (isinstance(other, PolicyPermissions) and
                other._policy == __tmp0._policy)


class __typ0(AbstractPermissions):
    """Owner permissions."""

    # pylint: disable=no-self-use

    def _entity_func(__tmp0) -> Callable[[str, str], __typ1]:
        """Return a function that can test entity access."""
        return lambda __tmp3, key: True


OwnerPermissions = __typ0()  # pylint: disable=invalid-name
