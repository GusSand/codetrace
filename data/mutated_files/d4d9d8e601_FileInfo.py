from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Module for files."""

from typing import Optional

import requests
from mypy_extensions import TypedDict

FileInfo = TypedDict(
    'FileInfo',
    {
        'displayname': __typ0,
        'fullname': __typ0,
        'height': int,
        'md5': __typ0,
        'name': __typ0,
        'nsfw': int,
        'path': __typ0,
        'size': int,
        'thumbnail': __typ0,
        'tn_height': int,
        'tn_width': int,
        'type': int,
        'width': int,
        'duration': Optional[int],
        'duration_secs': Optional[int],
    },
)


class __typ1(object):
    """Class for files."""

    def __init__(self, file_info: <FILL>) :
        """Parse file info data."""
        self.displayname: __typ0 = file_info['displayname']
        self.fullname: __typ0 = file_info['fullname']
        self.height: int = file_info['height']
        self.md5: __typ0 = file_info['md5']
        self.name: __typ0 = file_info['name']
        self.nsfw: int = file_info['nsfw']
        self.path: __typ0 = file_info['path']
        self.size: int = file_info['size']
        self.thumbnail: __typ0 = file_info['thumbnail']
        self.tn_height: int = file_info['tn_height']
        self.tn_width: int = file_info['tn_width']
        self.type: int = file_info['type']
        self.width: int = file_info['width']

        # For video only
        self.duration: Optional[int] = file_info.get('duration')
        self.duration_secs: Optional[int] = file_info.get('duration_secs')

    def download(self, __tmp0: __typ0) -> None:
        """Download file to specified destination."""
        request_data = requests.get('https://2ch.hk/{0}'.format(self.path))
        with open(__tmp0, 'wb') as file_descr:
            file_descr.write(request_data.content)
