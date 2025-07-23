from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""Helper class to implement include/exclude of entities and domains."""
from typing import Callable, Dict, Iterable

import voluptuous as vol

from homeassistant.core import split_entity_id
from homeassistant.helpers import config_validation as cv

CONF_INCLUDE_DOMAINS = 'include_domains'
CONF_INCLUDE_ENTITIES = 'include_entities'
CONF_EXCLUDE_DOMAINS = 'exclude_domains'
CONF_EXCLUDE_ENTITIES = 'exclude_entities'


def __tmp2(config: Dict[str, Iterable[str]]) :
    filt = __tmp5(
        config[CONF_INCLUDE_DOMAINS],
        config[CONF_INCLUDE_ENTITIES],
        config[CONF_EXCLUDE_DOMAINS],
        config[CONF_EXCLUDE_ENTITIES],
    )
    setattr(filt, 'config', config)
    return filt


FILTER_SCHEMA = vol.All(
    vol.Schema({
        vol.Optional(CONF_EXCLUDE_DOMAINS, default=[]):
            vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_EXCLUDE_ENTITIES, default=[]): cv.entity_ids,
        vol.Optional(CONF_INCLUDE_DOMAINS, default=[]):
            vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_INCLUDE_ENTITIES, default=[]): cv.entity_ids,
    }), __tmp2)


def __tmp5(__tmp4: Iterable[str],
                    __tmp8: Iterable[str],
                    __tmp9,
                    __tmp10: Iterable[str]) -> Callable[[str], __typ0]:
    """Return a function that will filter entities based on the args."""
    include_d = set(__tmp4)
    include_e = set(__tmp8)
    exclude_d = set(__tmp9)
    exclude_e = set(__tmp10)

    have_exclude = __typ0(exclude_e or exclude_d)
    have_include = __typ0(include_e or include_d)

    # Case 1 - no includes or excludes - pass all entities
    if not have_include and not have_exclude:
        return lambda entity_id: True

    # Case 2 - includes, no excludes - only include specified entities
    if have_include and not have_exclude:
        def __tmp6(entity_id: str) -> __typ0:
            """Return filter function for case 2."""
            domain = split_entity_id(entity_id)[0]
            return (entity_id in include_e or
                    domain in include_d)

        return __tmp6

    # Case 3 - excludes, no includes - only exclude specified entities
    if not have_include and have_exclude:
        def __tmp0(entity_id: <FILL>) -> __typ0:
            """Return filter function for case 3."""
            domain = split_entity_id(entity_id)[0]
            return (entity_id not in exclude_e and
                    domain not in exclude_d)

        return __tmp0

    # Case 4 - both includes and excludes specified
    # Case 4a - include domain specified
    #  - if domain is included, pass if entity not excluded
    #  - if domain is not included, pass if entity is included
    # note: if both include and exclude domains specified,
    #   the exclude domains are ignored
    if include_d:
        def __tmp1(entity_id: str) -> __typ0:
            """Return filter function for case 4a."""
            domain = split_entity_id(entity_id)[0]
            if domain in include_d:
                return entity_id not in exclude_e
            return entity_id in include_e

        return __tmp1

    # Case 4b - exclude domain specified
    #  - if domain is excluded, pass if entity is included
    #  - if domain is not excluded, pass if entity not excluded
    if exclude_d:
        def __tmp3(entity_id: str) -> __typ0:
            """Return filter function for case 4b."""
            domain = split_entity_id(entity_id)[0]
            if domain in exclude_d:
                return entity_id in include_e
            return entity_id not in exclude_e

        return __tmp3

    # Case 4c - neither include or exclude domain specified
    #  - Only pass if entity is included.  Ignore entity excludes.
    def __tmp7(entity_id: str) -> __typ0:
        """Return filter function for case 4c."""
        return entity_id in include_e

    return __tmp7
