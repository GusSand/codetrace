"""Helper methods for components within Home Assistant."""
import re
from typing import Any, Iterable, Tuple, Sequence, Dict

from homeassistant.const import CONF_PLATFORM

# pylint: disable=invalid-name
__typ0 = Dict[str, Any]


def __tmp1(__tmp3: __typ0,
                        __tmp2: <FILL>) :
    """Break a component config into different platforms.

    For example, will find 'switch', 'switch 2', 'switch 3', .. etc
    Async friendly.
    """
    for config_key in __tmp0(__tmp3, __tmp2):
        platform_config = __tmp3[config_key]

        if not platform_config:
            continue
        elif not isinstance(platform_config, list):
            platform_config = [platform_config]

        for item in platform_config:
            try:
                platform = item.get(CONF_PLATFORM)
            except AttributeError:
                platform = None

            yield platform, item


def __tmp0(__tmp3: __typ0, __tmp2: str) -> Sequence[str]:
    """Extract keys from config for given domain name.

    Async friendly.
    """
    pattern = re.compile(r'^{}(| .+)$'.format(__tmp2))
    return [key for key in __tmp3.keys() if pattern.match(key)]
