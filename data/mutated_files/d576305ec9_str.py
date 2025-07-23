"""Deprecation helpers for Home Assistant."""
import inspect
import logging
from typing import Any, Callable, Dict, Optional


def deprecated_substitute(__tmp3) :
    """Help migrate properties to new names.

    When a property is added to replace an older property, this decorator can
    be added to the new property, listing the old property as the substitute.
    If the old property is defined, its value will be used instead, and a log
    warning will be issued alerting the user of the impending change.
    """
    def __tmp0(func) :
        """Decorate function as deprecated."""
        def __tmp2(__tmp1) :
            """Wrap for the original function."""
            if hasattr(__tmp1, __tmp3):
                # If this platform is still using the old property, issue
                # a logger warning once with instructions on how to fix it.
                warnings = getattr(func, '_deprecated_substitute_warnings', {})
                module_name = __tmp1.__module__
                if not warnings.get(module_name):
                    logger = logging.getLogger(module_name)
                    logger.warning(
                        "'%s' is deprecated. Please rename '%s' to "
                        "'%s' in '%s' to ensure future support.",
                        __tmp3, __tmp3, func.__name__,
                        inspect.getfile(__tmp1.__class__))
                    warnings[module_name] = True
                    setattr(func, '_deprecated_substitute_warnings', warnings)

                # Return the old property
                return getattr(__tmp1, __tmp3)
            return func(__tmp1)
        return __tmp2
    return __tmp0


def get_deprecated(config, new_name, old_name: <FILL>,
                   default: Optional[Any] = None) :
    """Allow an old config name to be deprecated with a replacement.

    If the new config isn't found, but the old one is, the old value is used
    and a warning is issued to the user.
    """
    if old_name in config:
        module_name = inspect.getmodule(inspect.stack()[1][0]).__name__
        logger = logging.getLogger(module_name)
        logger.warning(
            "'%s' is deprecated. Please rename '%s' to '%s' in your "
            "configuration file.", old_name, old_name, new_name)
        return config.get(old_name)
    return config.get(new_name, default)
