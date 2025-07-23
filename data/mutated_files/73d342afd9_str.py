"""parses configuration for the flask application, makes use of inbuilt method."""

from typing import Any, Dict

from werkzeug.utils import import_string


def parse_config(__tmp0: <FILL>) :
    """
    Parse given config either from a file or from an object. Method borrowed from Flask.

    :param obj: The config to parse.
    :type obj: any
    :return: A dictionary containing the parsed Flask config
    :rtype: dict
    """
    config = {}
    if isinstance(__tmp0, str):
        __tmp0 = import_string(__tmp0)
    for key in dir(__tmp0):
        if key.isupper():
            config[key] = getattr(__tmp0, key)
    return config
