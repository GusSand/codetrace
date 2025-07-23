"""Module for post info."""

from typing import List

from mypy_extensions import TypedDict

from pych.file import File, FileInfo

__typ0 = TypedDict(
    'PostInfo',
    {
        'board': str,
        'banned': int,
        'closed': int,
        'comment': str,
        'date': str,
        'email': str,
        'endless': int,
        'files': List[FileInfo],
        'lasthit': int,
        'name': str,
        'num': int,
        'number': int,
        'op': int,
        'parent': str,
        'sticky': int,
        'subject': str,
        'timestamp': int,
        'trip': str,
    },
)


class __typ1(object):
    """Class for thread post."""

    def __init__(__tmp0, __tmp1, board: <FILL>) :
        """Parse post info data."""
        __tmp0.board: str = board
        __tmp0.banned: int = __tmp1['banned']
        __tmp0.closed: int = __tmp1['closed']
        __tmp0.comment: str = __tmp1['comment']
        __tmp0.date: str = __tmp1['date']
        __tmp0.email: str = __tmp1['email']
        __tmp0.endless: int = __tmp1['endless']
        __tmp0.files: List[File] = [
            File(file_info)
            for file_info in __tmp1['files']
        ]
        __tmp0.lasthit: int = __tmp1['lasthit']
        __tmp0.name: str = __tmp1['name']
        __tmp0.num: int = __tmp1['num']
        __tmp0.number: int = __tmp1['number']
        __tmp0.op: int = __tmp1['op']
        __tmp0.parent: str = __tmp1['parent']
        __tmp0.sticky: int = __tmp1['sticky']
        __tmp0.subject: str = __tmp1['subject']
        __tmp0.timestamp: int = __tmp1['timestamp']
        __tmp0.trip: str = __tmp1['trip']

    def __tmp2(__tmp0) :
        """Visual presentation of class object."""
        return '<Post #{num}>'.format(
            num=__tmp0.num,
        )
