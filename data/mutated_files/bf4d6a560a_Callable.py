from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"
"""Deprecation helpers for Home Assistant."""
import inspect
import logging
from typing import Any, Callable, Dict, Optional


def __tmp0(__tmp8: __typ0) -> Callable[..., Callable]:
    """Help migrate properties to new names.

    When a property is added to replace an older property, this decorator can
    be added to the new property, listing the old property as the substitute.
    If the old property is defined, its value will be used instead, and a log
    warning will be issued alerting the user of the impending change.
    """
    def __tmp2(func: <FILL>) -> Callable:
        """Decorate function as deprecated."""
        def __tmp6(__tmp1: Callable) -> __typ1:
            """Wrap for the original function."""
            if hasattr(__tmp1, __tmp8):
                # If this platform is still using the old property, issue
                # a logger warning once with instructions on how to fix it.
                warnings = getattr(func, '_deprecated_substitute_warnings', {})
                module_name = __tmp1.__module__
                if not warnings.get(module_name):
                    logger = logging.getLogger(module_name)
                    logger.warning(
                        "'%s' is deprecated. Please rename '%s' to "
                        "'%s' in '%s' to ensure future support.",
                        __tmp8, __tmp8, func.__name__,
                        inspect.getfile(__tmp1.__class__))
                    warnings[module_name] = True
                    setattr(func, '_deprecated_substitute_warnings', warnings)

                # Return the old property
                return getattr(__tmp1, __tmp8)
            return func(__tmp1)
        return __tmp6
    return __tmp2


def __tmp4(__tmp7: Dict[__typ0, __typ1], __tmp5: __typ0, __tmp3,
                   default: Optional[__typ1] = None) -> Optional[__typ1]:
    """Allow an old config name to be deprecated with a replacement.

    If the new config isn't found, but the old one is, the old value is used
    and a warning is issued to the user.
    """
    if __tmp3 in __tmp7:
        module_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        logger = logging.getLogger(module_name)
        logger.warning(
            "'%s' is deprecated. Please rename '%s' to '%s' in your "
            "configuration file.", __tmp3, __tmp3, __tmp5)
        return __tmp7.get(__tmp3)
    return __tmp7.get(__tmp5, default)
