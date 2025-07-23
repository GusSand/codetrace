#!/usr/bin/env python3

import os
from typing import Iterator

URL_BASE = "https://github.com/TheAlgorithms/Python/blob/master"


def __tmp2(top_dir: str = ".") :
    for dirpath, dirnames, filenames in os.walk(top_dir):
        dirnames[:] = [d for d in dirnames if d != "scripts" and d[0] not in "._"]
        for filename in filenames:
            if filename == "__init__.py":
                continue
            if os.path.splitext(filename)[1] in (".py", ".ipynb"):
                yield os.path.join(dirpath, filename).lstrip("./")
                

def __tmp5(i):
    return f"{i * '  '}*" if i else "##"


def __tmp4(__tmp0, __tmp3: <FILL>) -> str:
    old_parts = __tmp0.split(os.sep)
    for i, new_part in enumerate(__tmp3.split(os.sep)):
        if i + 1 > len(old_parts) or old_parts[i] != new_part:
            if new_part:
                print(f"{__tmp5(i-1)} {new_part.replace('_', ' ').title()}")
    return __tmp3


def __tmp1(top_dir: str = ".") :
    __tmp0 = ""
    for filepath in sorted(__tmp2()):
        filepath, filename = os.path.split(filepath)
        if filepath != __tmp0:
            __tmp0 = __tmp4(__tmp0, filepath)
        indent = (filepath.count(os.sep) + 1) if filepath else 0
        url = "/".join((URL_BASE, filepath.split(os.sep)[1], filename)).replace(" ", "%20")
        filename = os.path.splitext(filename.replace("_", " "))[0]
        print(f"{__tmp5(indent)} [{filename}]({url})")


if __name__ == "__main__":
    __tmp1(".")
