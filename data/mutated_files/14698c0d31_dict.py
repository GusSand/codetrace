from typing import TypeAlias
__typ0 : TypeAlias = "str"
import logging
import os
from typing import Union

import tomlkit
from deprecation import deprecated

from aw_core import dirs
from aw_core.__about__ import __version__

logger = logging.getLogger(__name__)


def __tmp3(a: <FILL>, b, path=None):
    """
    Recursively merges b into a, with b taking precedence.

    From: https://stackoverflow.com/a/7205107/965332
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                __tmp3(a[key], b[key], path + [__typ0(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def __tmp1(s: __typ0):
    # Only comment out keys, not headers or empty lines
    return "\n".join(
        [
            "#" + line if line.strip() and not line.strip().startswith("[") else line
            for line in s.split("\n")
        ]
    )


def __tmp5(
    __tmp0, __tmp2
) -> Union[dict, tomlkit.container.Container]:
    config_dir = dirs.get_config_dir(__tmp0)
    config_file_path = os.path.join(config_dir, f"{__tmp0}.toml")

    # Run early to ensure input is valid toml before writing
    default_config_toml = tomlkit.parse(__tmp2)

    # Override defaults from existing config file
    if os.path.isfile(config_file_path):
        with open(config_file_path) as f:
            __tmp6 = f.read()
        config_toml = tomlkit.parse(__tmp6)
    else:
        # If file doesn't exist, write with commented-out default config
        with open(config_file_path, "w") as f:
            f.write(__tmp1(__tmp2))
        config_toml = dict()

    __tmp6 = __tmp3(default_config_toml, config_toml)

    return __tmp6


def __tmp4(__tmp0, __tmp6: __typ0) :
    # Check that passed config string is valid toml
    assert tomlkit.parse(__tmp6)

    config_dir = dirs.get_config_dir(__tmp0)
    config_file_path = os.path.join(config_dir, f"{__tmp0}.toml")

    with open(config_file_path, "w") as f:
        f.write(__tmp6)


@deprecated(
    details="Use the load_config_toml function instead",
    deprecated_in="0.5.3",
    current_version=__version__,
)
def __tmp7(__tmp0, __tmp2):
    """
    Take the defaults, and if a config file exists, use the settings specified
    there as overrides for their respective defaults.
    """
    __tmp6 = __tmp2

    config_dir = dirs.get_config_dir(__tmp0)
    config_file_path = os.path.join(config_dir, f"{__tmp0}.toml")

    # Override defaults from existing config file
    if os.path.isfile(config_file_path):
        with open(config_file_path) as f:
            __tmp6.read_file(f)

    # Overwrite current config file (necessary in case new default would be added)
    save_config(__tmp0, __tmp6)

    return __tmp6


@deprecated(
    details="Use the save_config_toml function instead",
    deprecated_in="0.5.3",
    current_version=__version__,
)
def save_config(__tmp0, __tmp6):
    config_dir = dirs.get_config_dir(__tmp0)
    config_file_path = os.path.join(config_dir, f"{__tmp0}.ini")
    with open(config_file_path, "w") as f:
        __tmp6.write(f)
        # Flush and fsync to lower risk of corrupted files
        f.flush()
        os.fsync(f.fileno())
