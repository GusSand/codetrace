from typing import TypeAlias
__typ1 : TypeAlias = "bool"
"""Interface for accessing the file system with automatic caching.

The idea is to cache the results of any file system state reads during
a single transaction. This has two main benefits:

* This avoids redundant syscalls, as we won't perform the same OS
  operations multiple times.

* This makes it easier to reason about concurrent FS updates, as different
  operations targeting the same paths can't report different state during
  a transaction.

Note that this only deals with reading state, not writing.

Properties maintained by the API:

* The contents of the file are always from the same or later time compared
  to the reported mtime of the file, even if mtime is queried after reading
  a file.

* Repeating an operation produces the same result as the first one during
  a transaction.

* Call flush() to start a new transaction (flush the caches).

The API is a bit limited. It's easy to add new cached operations, however.
You should perform all file system reads through the API to actually take
advantage of the benefits.
"""

import os
import stat
from typing import Tuple, Dict, List, Optional
from mypy.util import read_with_python_encoding


class FileSystemMetaCache:
    def __tmp2(__tmp1) :
        __tmp1.flush()

    def flush(__tmp1) -> None:
        """Start another transaction and empty all caches."""
        __tmp1.stat_cache = {}  # type: Dict[str, os.stat_result]
        __tmp1.stat_error_cache = {}  # type: Dict[str, Exception]
        __tmp1.listdir_cache = {}  # type: Dict[str, List[str]]
        __tmp1.listdir_error_cache = {}  # type: Dict[str, Exception]
        __tmp1.isfile_case_cache = {}  # type: Dict[str, bool]

    def stat(__tmp1, path: <FILL>) :
        if path in __tmp1.stat_cache:
            return __tmp1.stat_cache[path]
        if path in __tmp1.stat_error_cache:
            raise __tmp1.stat_error_cache[path]
        try:
            st = os.stat(path)
        except Exception as err:
            __tmp1.stat_error_cache[path] = err
            raise
        __tmp1.stat_cache[path] = st
        return st

    def listdir(__tmp1, path) :
        if path in __tmp1.listdir_cache:
            return __tmp1.listdir_cache[path]
        if path in __tmp1.listdir_error_cache:
            raise __tmp1.listdir_error_cache[path]
        try:
            results = os.listdir(path)
        except Exception as err:
            __tmp1.listdir_error_cache[path] = err
            raise err
        __tmp1.listdir_cache[path] = results
        return results

    def isfile(__tmp1, path) :
        try:
            st = __tmp1.stat(path)
        except OSError:
            return False
        return stat.S_ISREG(st.st_mode)

    def __tmp0(__tmp1, path) :
        """Return whether path exists and is a file.

        On case-insensitive filesystems (like Mac or Windows) this returns
        False if the case of the path's last component does not exactly
        match the case found in the filesystem.
        TODO: We should maybe check the case for some directory components also,
        to avoid permitting wrongly-cased *packages*.
        """
        if path in __tmp1.isfile_case_cache:
            return __tmp1.isfile_case_cache[path]
        head, tail = os.path.split(path)
        if not tail:
            res = False
        else:
            try:
                names = __tmp1.listdir(head)
                res = tail in names and __tmp1.isfile(path)
            except OSError:
                res = False
        __tmp1.isfile_case_cache[path] = res
        return res

    def isdir(__tmp1, path: str) :
        try:
            st = __tmp1.stat(path)
        except OSError:
            return False
        return stat.S_ISDIR(st.st_mode)

    def __tmp3(__tmp1, path) :
        try:
            __tmp1.stat(path)
        except FileNotFoundError:
            return False
        return True


class __typ0(FileSystemMetaCache):
    def __tmp2(__tmp1, pyversion) :
        __tmp1.pyversion = pyversion
        __tmp1.flush()

    def flush(__tmp1) -> None:
        """Start another transaction and empty all caches."""
        super().flush()
        __tmp1.read_cache = {}  # type: Dict[str, str]
        __tmp1.read_error_cache = {}  # type: Dict[str, Exception]
        __tmp1.hash_cache = {}  # type: Dict[str, str]

    def read_with_python_encoding(__tmp1, path) :
        if path in __tmp1.read_cache:
            return __tmp1.read_cache[path]
        if path in __tmp1.read_error_cache:
            raise __tmp1.read_error_cache[path]

        # Need to stat first so that the contents of file are from no
        # earlier instant than the mtime reported by self.stat().
        __tmp1.stat(path)

        try:
            data, md5hash = read_with_python_encoding(path, __tmp1.pyversion)
        except Exception as err:
            __tmp1.read_error_cache[path] = err
            raise
        __tmp1.read_cache[path] = data
        __tmp1.hash_cache[path] = md5hash
        return data

    def md5(__tmp1, path: str) -> str:
        if path not in __tmp1.hash_cache:
            __tmp1.read_with_python_encoding(path)
        return __tmp1.hash_cache[path]
