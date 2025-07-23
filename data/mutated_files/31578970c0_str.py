"""JSON utility functions."""
import logging
from typing import Union, List, Dict

import json

from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)


def load_json(__tmp0) -> Union[List, Dict]:
    """Load JSON data from a file and return as dict or list.

    Defaults to returning empty dict if file is not found.
    """
    try:
        with open(__tmp0, encoding='utf-8') as fdesc:
            return json.loads(fdesc.read())
    except FileNotFoundError:
        # This is not a fatal error
        _LOGGER.debug('JSON file not found: %s', __tmp0)
    except ValueError as error:
        _LOGGER.exception('Could not parse JSON content: %s', __tmp0)
        raise HomeAssistantError(error)
    except OSError as error:
        _LOGGER.exception('JSON file reading failed: %s', __tmp0)
        raise HomeAssistantError(error)
    return {}  # (also evaluates to False)


def save_json(__tmp0: <FILL>, __tmp1):
    """Save JSON data to a file.

    Returns True on success.
    """
    try:
        data = json.dumps(__tmp1, sort_keys=True, indent=4)
        with open(__tmp0, 'w', encoding='utf-8') as fdesc:
            fdesc.write(data)
            return True
    except TypeError as error:
        _LOGGER.exception('Failed to serialize to JSON: %s',
                          __tmp0)
        raise HomeAssistantError(error)
    except OSError as error:
        _LOGGER.exception('Saving JSON file failed: %s',
                          __tmp0)
        raise HomeAssistantError(error)
    return False
