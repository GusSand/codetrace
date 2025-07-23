from typing import TypeAlias
__typ1 : TypeAlias = "str"
import json
from pathlib import Path

from aw_core.dirs import get_config_dir


class __typ0:
    def __tmp2(__tmp1, __tmp4: <FILL>):
        filename = "settings.json" if not __tmp4 else "settings-testing.json"
        __tmp1.config_file = Path(get_config_dir("aw-server")) / filename
        __tmp1.load()

    def __tmp0(__tmp1, __tmp3):
        return __tmp1.get(__tmp3)

    def __setitem__(__tmp1, __tmp3, value):
        return __tmp1.set(__tmp3, value)

    def load(__tmp1):
        if __tmp1.config_file.exists():
            with open(__tmp1.config_file) as f:
                __tmp1.data = json.load(f)
        else:
            __tmp1.data = {}

    def save(__tmp1):
        with open(__tmp1.config_file, "w") as f:
            json.dump(__tmp1.data, f, indent=4)

    def get(__tmp1, __tmp3, default=None):
        if not __tmp3:
            return __tmp1.data
        return __tmp1.data.get(__tmp3, default)

    def set(__tmp1, __tmp3, value):
        if value:
            __tmp1.data[__tmp3] = value
        else:
            if __tmp3 in __tmp1.data:
                del __tmp1.data[__tmp3]
        __tmp1.save()
