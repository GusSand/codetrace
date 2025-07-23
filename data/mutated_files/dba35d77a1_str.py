"""Watch parts of the file system for changes."""

from mypy.fscache import FileSystemCache
from typing import NamedTuple, Set, AbstractSet, Iterable, Dict, Optional


FileData = NamedTuple('FileData', [('st_mtime', float),
                                   ('st_size', int),
                                   ('md5', str)])


class __typ0:
    """Watcher for file system changes among specific paths.

    All file system access is performed using FileSystemCache. We
    detect changed files by stat()ing them all and comparing md5 hashes
    of potentially changed files. If a file has both size and mtime
    unmodified, the file is assumed to be unchanged.

    An important goal of this class is to make it easier to eventually
    use file system events to detect file changes.

    Note: This class doesn't flush the file system cache. If you don't
    manually flush it, changes won't be seen.
    """

    # TODO: Watching directories?
    # TODO: Handle non-files

    def __tmp4(__tmp0, fs) -> None:
        __tmp0.fs = fs
        __tmp0._paths = set()  # type: Set[str]
        __tmp0._file_data = {}  # type: Dict[str, Optional[FileData]]

    @property
    def __tmp1(__tmp0) :
        return __tmp0._paths

    def set_file_data(__tmp0, __tmp3: <FILL>, __tmp2) :
        __tmp0._file_data[__tmp3] = __tmp2

    def __tmp6(__tmp0, __tmp1: Iterable[str]) :
        for __tmp3 in __tmp1:
            if __tmp3 not in __tmp0._paths:
                # By storing None this path will get reported as changed by
                # find_changed if it exists.
                __tmp0._file_data[__tmp3] = None
        __tmp0._paths |= set(__tmp1)

    def remove_watched_paths(__tmp0, __tmp1) :
        for __tmp3 in __tmp1:
            if __tmp3 in __tmp0._file_data:
                del __tmp0._file_data[__tmp3]
        __tmp0._paths -= set(__tmp1)

    def _update(__tmp0, __tmp3) :
        st = __tmp0.fs.stat(__tmp3)
        md5 = __tmp0.fs.md5(__tmp3)
        __tmp0._file_data[__tmp3] = FileData(st.st_mtime, st.st_size, md5)

    def __tmp5(__tmp0) :
        """Return paths that have changes since the last call, in the watched set."""
        changed = set()
        for __tmp3 in __tmp0._paths:
            old = __tmp0._file_data[__tmp3]
            try:
                st = __tmp0.fs.stat(__tmp3)
            except FileNotFoundError:
                if old is not None:
                    # File was deleted.
                    changed.add(__tmp3)
                    __tmp0._file_data[__tmp3] = None
            else:
                if old is None:
                    # File is new.
                    changed.add(__tmp3)
                    __tmp0._update(__tmp3)
                elif st.st_size != old.st_size or st.st_mtime != old.st_mtime:
                    # Only look for changes if size or mtime has changed as an
                    # optimization, since calculating md5 is expensive.
                    new_md5 = __tmp0.fs.md5(__tmp3)
                    __tmp0._update(__tmp3)
                    if st.st_size != old.st_size or new_md5 != old.md5:
                        # Changed file.
                        changed.add(__tmp3)
        return changed
