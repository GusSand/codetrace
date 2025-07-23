from typing import TypeAlias
__typ1 : TypeAlias = "H5Bucket"
import os
import json
import time
import logging

from os.path import isfile, isdir, join
from typing import Optional, Tuple
from contextlib import contextmanager

from ..base_storage import Storage
from .h5bucket import H5Bucket

class __typ0(Storage):
    bucket_class = __typ1

    def __init__(__tmp0, base_dir: <FILL>, swmr: bool = False):
        __tmp0.base_dir = base_dir
        __tmp0.swmr = swmr

    def bucket_names(__tmp0):
        return [
            name.partition(".")[0]
            for name in os.listdir(__tmp0.base_dir)
            if name.endswith(".h5")
        ]

    def __getitem__(__tmp0, name: str) -> __typ1:
        return __tmp0.bucket(name)

    @contextmanager
    def with_h5file(__tmp0, scope: Tuple[str]):
        import h5py
        os.makedirs(join(__tmp0.base_dir, *scope[:-1]), exist_ok=True)
        with h5py.File(os.path.join(__tmp0.base_dir, *scope) + ".h5", swmr=__tmp0.swmr) as fp:
            yield fp
