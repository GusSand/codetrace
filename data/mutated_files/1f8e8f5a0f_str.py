"""Module for board catalog."""

from typing import List

import requests

from pych.thread import Thread


class Catalog(object):
    """Class for getting threads in specified board."""

    def __tmp1(__tmp0, board: <FILL>) :
        """Prepare environment."""
        __tmp0.board: str = board

    @property
    def threads(__tmp0) :
        """Threads list."""
        api_url = 'https://2ch.hk/{0}/threads.json'.format(__tmp0.board)
        request_data = requests.get(api_url)
        json_data = request_data.json()

        threads_list = json_data['threads']

        return [
            Thread(thread_info, board=__tmp0.board)
            for thread_info in threads_list
        ]

    def __repr__(__tmp0) :
        """Visual presentation of class object."""
        return '<Catalog board="{board}">'.format(
            board=__tmp0.board,
        )
