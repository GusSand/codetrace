from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"
"""Deprecation helpers for Home Assistant."""
import inspect
import logging
from typing import Any, Callable, Dict, Optional


def deprecated_substitute(__tmp4: __typ0) :
    """Help migrate properties to new names.

    When a property is added to replace an older property, this decorator can
    be added to the new property, listing the old property as the substitute.
    If the old property is defined, its value will be used instead, and a log
    warning will be issued alerting the user of the impending change.
    """
    def __tmp1(__tmp3) -> Callable:
        """Decorate function as deprecated."""
        def func_wrapper(__tmp0: <FILL>) :
            """Wrap for the original function."""
            if hasattr(__tmp0, __tmp4):
                # If this platform is still using the old property, issue
                # a logger warning once with instructions on how to fix it.
                warnings = getattr(__tmp3, '_deprecated_substitute_warnings', {})
                module_name = __tmp0.__module__
                if not warnings.get(module_name):
                    logger = logging.getLogger(module_name)
                    logger.warning(
                        "'%s' is deprecated. Please rename '%s' to "
                        "'%s' in '%s' to ensure future support.",
                        __tmp4, __tmp4, __tmp3.__name__,
                        inspect.getfile(__tmp0.__class__))
                    warnings[module_name] = True
                    setattr(__tmp3, '_deprecated_substitute_warnings', warnings)

                # Return the old property
                return getattr(__tmp0, __tmp4)
            return __tmp3(__tmp0)
        return func_wrapper
    return __tmp1


def __tmp2(config, new_name: __typ0, old_name: __typ0,
                   default: Optional[__typ1] = None) :
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
