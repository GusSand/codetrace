from typing import TypeAlias
__typ3 : TypeAlias = "SafeConstructor"
"""ruamel.yaml utility functions."""
import logging
import os
from os import O_CREAT, O_TRUNC, O_WRONLY, stat_result
from collections import OrderedDict
from typing import Union, List, Dict

import ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
from ruamel.yaml.error import YAMLError
from ruamel.yaml.compat import StringIO

from homeassistant.util.yaml import secret_yaml
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)

__typ2 = Union[List, Dict, str]  # pylint: disable=invalid-name


class ExtSafeConstructor(__typ3):
    """Extended SafeConstructor."""


class __typ1(HomeAssistantError):
    """Unsupported YAML."""


class __typ0(HomeAssistantError):
    """Error writing the data."""


def __tmp1(constructor, __tmp6) \
        :
    """Load another YAML file and embeds it using the !include tag.

    Example:
        device_tracker: !include device_tracker.yaml
    """
    __tmp5 = os.path.join(os.path.dirname(constructor.name), __tmp6.value)
    return __tmp0(__tmp5, False)


def _yaml_unsupported(constructor, __tmp6) :
    raise __typ1(
        'Unsupported YAML, you can not use {} in {}'
        .format(__tmp6.tag, os.path.basename(constructor.name)))


def __tmp4(__tmp2) -> str:
    """Create yaml string from object."""
    yaml = YAML(typ='rt')
    yaml.indent(sequence=4, offset=2)
    stream = StringIO()
    try:
        yaml.dump(__tmp2, stream)
        result = stream.getvalue()  # type: str
        return result
    except YAMLError as exc:
        _LOGGER.error("YAML error: %s", exc)
        raise HomeAssistantError(exc)


def __tmp3(__tmp2) :
    """Create object from yaml string."""
    yaml = YAML(typ='rt')
    try:
        result = yaml.load(__tmp2)  # type: Union[List, Dict, str]
        return result
    except YAMLError as exc:
        _LOGGER.error("YAML error: %s", exc)
        raise HomeAssistantError(exc)


def __tmp0(__tmp5, round_trip: bool = False) :
    """Load a YAML file."""
    if round_trip:
        yaml = YAML(typ='rt')
        yaml.preserve_quotes = True
    else:
        if not hasattr(ExtSafeConstructor, 'name'):
            ExtSafeConstructor.name = __tmp5
        yaml = YAML(typ='safe')
        yaml.Constructor = ExtSafeConstructor

    try:
        with open(__tmp5, encoding='utf-8') as conf_file:
            # If configuration file is empty YAML returns None
            # We convert that to an empty dict
            return yaml.load(conf_file) or OrderedDict()
    except YAMLError as exc:
        _LOGGER.error("YAML error in %s: %s", __tmp5, exc)
        raise HomeAssistantError(exc)
    except UnicodeDecodeError as exc:
        _LOGGER.error("Unable to read file %s: %s", __tmp5, exc)
        raise HomeAssistantError(exc)


def save_yaml(__tmp5: <FILL>, __tmp2) :
    """Save a YAML file."""
    yaml = YAML(typ='rt')
    yaml.indent(sequence=4, offset=2)
    tmp_fname = __tmp5 + "__TEMP__"
    try:
        try:
            file_stat = os.stat(__tmp5)
        except OSError:
            file_stat = stat_result(
                (0o644, -1, -1, -1, -1, -1, -1, -1, -1, -1))
        with open(os.open(tmp_fname, O_WRONLY | O_CREAT | O_TRUNC,
                          file_stat.st_mode), 'w', encoding='utf-8') \
                as temp_file:
            yaml.dump(__tmp2, temp_file)
        os.replace(tmp_fname, __tmp5)
        if hasattr(os, 'chown') and file_stat.st_ctime > -1:
            try:
                os.chown(__tmp5, file_stat.st_uid, file_stat.st_gid)
            except OSError:
                pass
    except YAMLError as exc:
        _LOGGER.error(str(exc))
        raise HomeAssistantError(exc)
    except OSError as exc:
        _LOGGER.exception('Saving YAML file %s failed: %s', __tmp5, exc)
        raise __typ0(exc)
    finally:
        if os.path.exists(tmp_fname):
            try:
                os.remove(tmp_fname)
            except OSError as exc:
                # If we are cleaning up then something else went wrong, so
                # we should suppress likely follow-on errors in the cleanup
                _LOGGER.error("YAML replacement cleanup failed: %s", exc)


ExtSafeConstructor.add_constructor(u'!secret', secret_yaml)
ExtSafeConstructor.add_constructor(u'!include', __tmp1)
ExtSafeConstructor.add_constructor(None, _yaml_unsupported)
