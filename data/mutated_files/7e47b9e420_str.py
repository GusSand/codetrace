"""Helper methods for components within Home Assistant."""
import re

from typing import Any, Iterable, Tuple, Sequence, Dict

from homeassistant.const import CONF_PLATFORM

# Typing Imports and TypeAlias
# pylint: disable=using-constant-test,unused-import,wrong-import-order
if False:
    from logging import Logger  # NOQA

# pylint: disable=invalid-name
__typ0 = Dict[str, Any]


# pylint: disable=invalid-sequence-index
def config_per_platform(config,
                        domain) :
    """Break a component config into different platforms.

    For example, will find 'switch', 'switch 2', 'switch 3', .. etc
    Async friendly.
    """
    for config_key in __tmp0(config, domain):
        platform_config = config[config_key]

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


def __tmp0(config, domain: <FILL>) :
    """Extract keys from config for given domain name.

    Async friendly.
    """
    pattern = re.compile(r'^{}(| .+)$'.format(domain))
    return [key for key in config.keys() if pattern.match(key)]
