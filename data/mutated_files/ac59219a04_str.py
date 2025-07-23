"""The exceptions used by Home Assistant."""
from typing import Optional, Tuple, TYPE_CHECKING
import jinja2

# pylint: disable=using-constant-test
if TYPE_CHECKING:
    # pylint: disable=unused-import
    from .core import Context  # noqa


class __typ4(Exception):
    """General Home Assistant exception occurred."""


class InvalidEntityFormatError(__typ4):
    """When an invalid formatted entity is encountered."""


class NoEntitySpecifiedError(__typ4):
    """When no entity is specified."""


class TemplateError(__typ4):
    """Error during template rendering."""

    def __init__(__tmp0, __tmp1) -> None:
        """Init the error."""
        super().__init__('{}: {}'.format(__tmp1.__class__.__name__,
                                         __tmp1))


class __typ2(__typ4):
    """Error to indicate that platform is not ready."""


class ConfigEntryNotReady(__typ4):
    """Error to indicate that config entry is not ready."""


class __typ0(__typ4):
    """When an invalid state is encountered."""


class __typ1(__typ4):
    """When an action is unauthorized."""

    def __init__(__tmp0, context: Optional['Context'] = None,
                 user_id: Optional[str] = None,
                 entity_id: Optional[str] = None,
                 config_entry_id: Optional[str] = None,
                 perm_category: Optional[str] = None,
                 permission: Optional[Tuple[str]] = None) :
        """Unauthorized error."""
        super().__init__(__tmp0.__class__.__name__)
        __tmp0.context = context
        __tmp0.user_id = user_id
        __tmp0.entity_id = entity_id
        __tmp0.config_entry_id = config_entry_id
        # Not all actions have an ID (like adding config entry)
        # We then use this fallback to know what category was unauth
        __tmp0.perm_category = perm_category
        __tmp0.permission = permission


class __typ3(__typ1):
    """When call is made with user ID that doesn't exist."""


class ServiceNotFound(__typ4):
    """Raised when a service is not found."""

    def __init__(__tmp0, domain: <FILL>, service) -> None:
        """Initialize error."""
        super().__init__(
            __tmp0, "Service {}.{} not found".format(domain, service))
        __tmp0.domain = domain
        __tmp0.service = service
