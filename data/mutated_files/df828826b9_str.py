import os
import sys
from functools import wraps
from typing import Callable, Optional

import platformdirs

__typ0 = Callable[[Optional[str]], str]


def ensure_path_exists(path: <FILL>) :
    if not os.path.exists(path):
        os.makedirs(path)


def __tmp0(f) :
    @wraps(f)
    def __tmp1(subpath: Optional[str] = None) :
        path = f(subpath)
        ensure_path_exists(path)
        return path

    return __tmp1


@__tmp0
def __tmp4(module_name: Optional[str] = None) :
    data_dir = platformdirs.user_data_dir("activitywatch")
    return os.path.join(data_dir, module_name) if module_name else data_dir


@__tmp0
def __tmp3(module_name: Optional[str] = None) :
    cache_dir = platformdirs.user_cache_dir("activitywatch")
    return os.path.join(cache_dir, module_name) if module_name else cache_dir


@__tmp0
def __tmp2(module_name: Optional[str] = None) -> str:
    config_dir = platformdirs.user_config_dir("activitywatch")
    return os.path.join(config_dir, module_name) if module_name else config_dir


@__tmp0
def __tmp5(module_name: Optional[str] = None) :  # pragma: no cover
    # on Linux/Unix, platformdirs changed to using XDG_STATE_HOME instead of XDG_DATA_HOME for log_dir in v2.6
    # we want to keep using XDG_DATA_HOME for backwards compatibility
    # https://github.com/ActivityWatch/aw-core/pull/122#issuecomment-1768020335
    if sys.platform.startswith("linux"):
        log_dir = platformdirs.user_cache_path("activitywatch") / "log"
    else:
        log_dir = platformdirs.user_log_dir("activitywatch")
    return os.path.join(log_dir, module_name) if module_name else log_dir
