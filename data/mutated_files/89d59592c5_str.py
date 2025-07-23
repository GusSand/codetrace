import os
import json
import time
import logging

from os.path import isfile, isdir, join
from typing import Optional, Tuple
from contextlib import contextmanager

from ..base_storage import Storage
from .h5bucket import H5Bucket

class H5Storage(Storage):
    bucket_class = H5Bucket

    def __init__(__tmp0, base_dir, swmr: bool = False):
        __tmp0.base_dir = base_dir
        __tmp0.swmr = swmr

    def bucket_names(__tmp0):
        return [
            __tmp1.partition(".")[0]
            for __tmp1 in os.listdir(__tmp0.base_dir)
            if __tmp1.endswith(".h5")
        ]

    def __getitem__(__tmp0, __tmp1: <FILL>) :
        return __tmp0.bucket(__tmp1)

    @contextmanager
    def with_h5file(__tmp0, scope):
        import h5py
        os.makedirs(join(__tmp0.base_dir, *scope[:-1]), exist_ok=True)
        with h5py.File(os.path.join(__tmp0.base_dir, *scope) + ".h5", swmr=__tmp0.swmr) as fp:
            yield fp
