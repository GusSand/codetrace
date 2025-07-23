from typing import TypeAlias
__typ0 : TypeAlias = "Callable"
"""Deprecation helpers for Home Assistant."""
import inspect
import logging
from typing import Any, Callable, Dict, Optional


def deprecated_substitute(__tmp3) -> __typ0[..., __typ0]:
    """Help migrate properties to new names.

    When a property is added to replace an older property, this decorator can
    be added to the new property, listing the old property as the substitute.
    If the old property is defined, its value will be used instead, and a log
    warning will be issued alerting the user of the impending change.
    """
    def decorator(__tmp1) -> __typ0:
        """Decorate function as deprecated."""
        def func_wrapper(self: __typ0) -> Any:
            """Wrap for the original function."""
            if hasattr(self, __tmp3):
                # If this platform is still using the old property, issue
                # a logger warning once with instructions on how to fix it.
                warnings = getattr(__tmp1, '_deprecated_substitute_warnings', {})
                module_name = self.__module__
                if not warnings.get(module_name):
                    logger = logging.getLogger(module_name)
                    logger.warning(
                        "'%s' is deprecated. Please rename '%s' to "
                        "'%s' in '%s' to ensure future support.",
                        __tmp3, __tmp3, __tmp1.__name__,
                        inspect.getfile(self.__class__))
                    warnings[module_name] = True
                    setattr(__tmp1, '_deprecated_substitute_warnings', warnings)

                # Return the old property
                return getattr(self, __tmp3)
            return __tmp1(self)
        return func_wrapper
    return decorator


def __tmp2(config: Dict[str, Any], new_name: <FILL>, __tmp0,
                   default: Optional[Any] = None) -> Optional[Any]:
    """Allow an old config name to be deprecated with a replacement.

    If the new config isn't found, but the old one is, the old value is used
    and a warning is issued to the user.
    """
    if __tmp0 in config:
        module_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        logger = logging.getLogger(module_name)
        logger.warning(
            "'%s' is deprecated. Please rename '%s' to '%s' in your "
            "configuration file.", __tmp0, __tmp0, new_name)
        return config.get(__tmp0)
    return config.get(new_name, default)
