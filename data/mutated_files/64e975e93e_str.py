#!/usr/bin/env python3
"""Merge all translation sources into a single JSON file."""
import glob
import json
import os
import re
from typing import Union, List, Dict

FILENAME_FORMAT = re.compile(r'strings\.(?P<suffix>\w+)\.json')


def __tmp1(__tmp11) \
        -> Union[List, Dict]:
    """Load JSON data from a file and return as dict or list.

    Defaults to returning empty dict if file is not found.
    """
    with open(__tmp11, encoding='utf-8') as fdesc:
        return json.loads(fdesc.read())
    return {}


def __tmp6(__tmp11: <FILL>, __tmp2):
    """Save JSON data to a file.

    Returns True on success.
    """
    __tmp2 = json.dumps(__tmp2, sort_keys=True, indent=4)
    with open(__tmp11, 'w', encoding='utf-8') as fdesc:
        fdesc.write(__tmp2)
        return True
    return False


def __tmp10(path):
    """Get the language code for the given file path."""
    return os.path.splitext(os.path.basename(path))[0]


def __tmp12(__tmp9, __tmp7):
    """Get the component translation path."""
    if os.path.isdir(os.path.join("homeassistant", "components", __tmp7)):
        return os.path.join(
            "homeassistant", "components", __tmp7, ".translations",
            "{}.json".format(__tmp9))
    else:
        return os.path.join(
            "homeassistant", "components", ".translations",
            "{}.{}.json".format(__tmp7, __tmp9))


def __tmp13(__tmp9, __tmp7, __tmp5):
    """Get the platform translation path."""
    if os.path.isdir(os.path.join(
            "homeassistant", "components", __tmp7, __tmp5)):
        return os.path.join(
            "homeassistant", "components", __tmp7, __tmp5,
            ".translations", "{}.json".format(__tmp9))
    else:
        return os.path.join(
            "homeassistant", "components", __tmp7, ".translations",
            "{}.{}.json".format(__tmp5, __tmp9))


def __tmp4(__tmp3):
    """Get the component level translations."""
    __tmp3 = __tmp3.copy()
    __tmp3.pop('platform', None)

    return __tmp3


def __tmp8(__tmp9, __tmp3):
    """Distribute the translations for this language."""
    components = __tmp3.get('component', {})
    for __tmp7, component_translations in components.items():
        base_translations = __tmp4(component_translations)
        if base_translations:
            path = __tmp12(__tmp9, __tmp7)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            __tmp6(path, base_translations)

        for __tmp5, platform_translations in component_translations.get(
                'platform', {}).items():
            path = __tmp13(__tmp9, __tmp7, __tmp5)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            __tmp6(path, platform_translations)


def __tmp0():
    """Run the script."""
    if not os.path.isfile("requirements_all.txt"):
        print("Run this from HA root dir")
        return

    paths = glob.iglob("build/translations-download/*.json")
    for path in paths:
        __tmp9 = __tmp10(path)
        __tmp3 = __tmp1(path)
        __tmp8(__tmp9, __tmp3)


if __name__ == '__main__':
    __tmp0()
