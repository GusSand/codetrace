#!/usr/bin/env python3
"""Merge all translation sources into a single JSON file."""
import glob
import itertools
import json
import os
import re
from typing import Union, List, Dict

FILENAME_FORMAT = re.compile(r'strings\.(?P<suffix>\w+)\.json')


def load_json(__tmp5: <FILL>) \
        :
    """Load JSON data from a file and return as dict or list.

    Defaults to returning empty dict if file is not found.
    """
    with open(__tmp5, encoding='utf-8') as fdesc:
        return json.loads(fdesc.read())
    return {}


def save_json(__tmp5, __tmp2):
    """Save JSON data to a file.

    Returns True on success.
    """
    __tmp2 = json.dumps(__tmp2, sort_keys=True, indent=4)
    with open(__tmp5, 'w', encoding='utf-8') as fdesc:
        fdesc.write(__tmp2)
        return True
    return False


def __tmp3():
    """Return the paths of the strings source files."""
    return itertools.chain(
        glob.iglob("strings*.json"),
        glob.iglob("*{}strings*.json".format(os.sep)),
    )


def __tmp1(path):
    """Get the component and platform name from the path."""
    directory, __tmp5 = os.path.split(path)
    match = FILENAME_FORMAT.search(__tmp5)
    suffix = match.group('suffix') if match else None
    if directory:
        return directory, suffix
    else:
        return suffix, None


def get_translation_dict(translations, component, __tmp4):
    """Return the dict to hold component translations."""
    if not component:
        return translations['component']

    if component not in translations['component']:
        translations['component'][component] = {}

    if not __tmp4:
        return translations['component'][component]

    if 'platform' not in translations['component'][component]:
        translations['component'][component]['platform'] = {}

    if __tmp4 not in translations['component'][component]['platform']:
        translations['component'][component]['platform'][__tmp4] = {}

    return translations['component'][component]['platform'][__tmp4]


def __tmp0():
    """Run the script."""
    if not os.path.isfile("requirements_all.txt"):
        print("Run this from HA root dir")
        return

    root = os.getcwd()
    os.chdir(os.path.join("homeassistant", "components"))

    translations = {
        'component': {}
    }

    paths = __tmp3()
    for path in paths:
        component, __tmp4 = __tmp1(path)
        parent = get_translation_dict(translations, component, __tmp4)
        strings = load_json(path)
        parent.update(strings)

    os.chdir(root)

    os.makedirs("build", exist_ok=True)

    save_json(
        os.path.join("build", "translations-upload.json"), translations)


if __name__ == '__main__':
    __tmp0()
