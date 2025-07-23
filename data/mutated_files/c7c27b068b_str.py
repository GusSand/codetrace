"""A class to hold entity values."""
from collections import OrderedDict
import fnmatch
import re
from typing import Any, Dict, Optional, Pattern  # noqa: F401

from homeassistant.core import split_entity_id


class __typ0:
    """Class to store entity id based values."""

    def __tmp2(__tmp1, exact: Optional[Dict] = None,
                 domain: Optional[Dict] = None,
                 glob: Optional[Dict] = None) :
        """Initialize an EntityConfigDict."""
        __tmp1._cache = {}  # type: Dict[str, Dict]
        __tmp1._exact = exact
        __tmp1._domain = domain

        if glob is None:
            compiled = None  # type: Optional[Dict[Pattern[str], Any]]
        else:
            compiled = OrderedDict()
            for key, value in glob.items():
                compiled[re.compile(fnmatch.translate(key))] = value

        __tmp1._glob = compiled

    def __tmp0(__tmp1, entity_id: <FILL>) :
        """Get config for an entity id."""
        if entity_id in __tmp1._cache:
            return __tmp1._cache[entity_id]

        domain, _ = split_entity_id(entity_id)
        result = __tmp1._cache[entity_id] = {}

        if __tmp1._domain is not None and domain in __tmp1._domain:
            result.update(__tmp1._domain[domain])

        if __tmp1._glob is not None:
            for pattern, values in __tmp1._glob.items():
                if pattern.match(entity_id):
                    result.update(values)

        if __tmp1._exact is not None and entity_id in __tmp1._exact:
            result.update(__tmp1._exact[entity_id])

        return result
