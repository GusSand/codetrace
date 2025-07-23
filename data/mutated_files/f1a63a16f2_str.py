from typing import TypeAlias
__typ2 : TypeAlias = "bool"
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


class __typ0:
    def __init__(__tmp0) -> None:
        __tmp0.flush()

    def flush(__tmp0) -> None:
        """Start another transaction and empty all caches."""
        __tmp0.stat_cache = {}  # type: Dict[str, os.stat_result]
        __tmp0.stat_error_cache = {}  # type: Dict[str, Exception]
        __tmp0.listdir_cache = {}  # type: Dict[str, List[str]]
        __tmp0.listdir_error_cache = {}  # type: Dict[str, Exception]
        __tmp0.isfile_case_cache = {}  # type: Dict[str, bool]

    def stat(__tmp0, path) -> os.stat_result:
        if path in __tmp0.stat_cache:
            return __tmp0.stat_cache[path]
        if path in __tmp0.stat_error_cache:
            raise __tmp0.stat_error_cache[path]
        try:
            st = os.stat(path)
        except Exception as err:
            __tmp0.stat_error_cache[path] = err
            raise
        __tmp0.stat_cache[path] = st
        return st

    def listdir(__tmp0, path: str) -> List[str]:
        if path in __tmp0.listdir_cache:
            return __tmp0.listdir_cache[path]
        if path in __tmp0.listdir_error_cache:
            raise __tmp0.listdir_error_cache[path]
        try:
            results = os.listdir(path)
        except Exception as err:
            __tmp0.listdir_error_cache[path] = err
            raise err
        __tmp0.listdir_cache[path] = results
        return results

    def isfile(__tmp0, path: str) -> __typ2:
        try:
            st = __tmp0.stat(path)
        except OSError:
            return False
        return stat.S_ISREG(st.st_mode)

    def isfile_case(__tmp0, path: str) :
        """Return whether path exists and is a file.

        On case-insensitive filesystems (like Mac or Windows) this returns
        False if the case of the path's last component does not exactly
        match the case found in the filesystem.
        TODO: We should maybe check the case for some directory components also,
        to avoid permitting wrongly-cased *packages*.
        """
        if path in __tmp0.isfile_case_cache:
            return __tmp0.isfile_case_cache[path]
        head, tail = os.path.split(path)
        if not tail:
            res = False
        else:
            try:
                names = __tmp0.listdir(head)
                res = tail in names and __tmp0.isfile(path)
            except OSError:
                res = False
        __tmp0.isfile_case_cache[path] = res
        return res

    def isdir(__tmp0, path) -> __typ2:
        try:
            st = __tmp0.stat(path)
        except OSError:
            return False
        return stat.S_ISDIR(st.st_mode)

    def exists(__tmp0, path: <FILL>) -> __typ2:
        try:
            __tmp0.stat(path)
        except FileNotFoundError:
            return False
        return True


class __typ1(__typ0):
    def __init__(__tmp0, pyversion: Tuple[int, int]) -> None:
        __tmp0.pyversion = pyversion
        __tmp0.flush()

    def flush(__tmp0) -> None:
        """Start another transaction and empty all caches."""
        super().flush()
        __tmp0.read_cache = {}  # type: Dict[str, str]
        __tmp0.read_error_cache = {}  # type: Dict[str, Exception]
        __tmp0.hash_cache = {}  # type: Dict[str, str]

    def read_with_python_encoding(__tmp0, path: str) -> str:
        if path in __tmp0.read_cache:
            return __tmp0.read_cache[path]
        if path in __tmp0.read_error_cache:
            raise __tmp0.read_error_cache[path]

        # Need to stat first so that the contents of file are from no
        # earlier instant than the mtime reported by self.stat().
        __tmp0.stat(path)

        try:
            data, md5hash = read_with_python_encoding(path, __tmp0.pyversion)
        except Exception as err:
            __tmp0.read_error_cache[path] = err
            raise
        __tmp0.read_cache[path] = data
        __tmp0.hash_cache[path] = md5hash
        return data

    def md5(__tmp0, path: str) -> str:
        if path not in __tmp0.hash_cache:
            __tmp0.read_with_python_encoding(path)
        return __tmp0.hash_cache[path]
