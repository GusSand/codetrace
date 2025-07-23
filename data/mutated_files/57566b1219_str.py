"""Module for threads."""

from typing import List

import requests
from mypy_extensions import TypedDict

from pych.post import Post

ThreadInfo = TypedDict(
    'ThreadInfo',
    {
        'board': str,
        'comment': str,
        'lasthit': int,
        'num': str,
        'posts_count': int,
        'score': float,
        'subject': str,
        'timestamp': int,
        'views': int,
    },
)


class Thread(object):
    """Thread object."""

    def __tmp2(__tmp1, thread_info, board: <FILL>) :
        """Parse kwargs arguments."""
        __tmp1.board: str = board
        __tmp1.comment: str = thread_info['comment']
        __tmp1.lasthit: int = thread_info['lasthit']
        __tmp1.num: str = thread_info['num']
        __tmp1.posts_count: int = thread_info['posts_count']
        __tmp1.score: float = thread_info['score']
        __tmp1.subject: str = thread_info['subject']
        __tmp1.timestamp: int = thread_info['timestamp']
        __tmp1.views: int = thread_info['views']

        __tmp1.url = '/{board}/{num}.html'.format(
            board=__tmp1.board,
            num=__tmp1.num,
        )

    @property
    def __tmp3(__tmp1) :
        """Thread posts list."""
        api_url = 'https://2ch.hk/{board}/res/{num}.json'.format(
            board=__tmp1.board,
            num=__tmp1.num,
        )

        request_data = requests.get(api_url)
        json_data = request_data.json()

        posts_list = json_data['threads'].pop()['posts']

        return [
            Post(post_info, board=__tmp1.board)
            for post_info in posts_list
        ]

    def __tmp0(__tmp1) -> str:
        """Visual presentation of class object."""
        max_subject_length = 32

        return '<Thread board="{board}" #{num} "{subject}">'.format(
            board=__tmp1.board,
            num=__tmp1.num,
            subject=__tmp1.subject[:max_subject_length],
        )
