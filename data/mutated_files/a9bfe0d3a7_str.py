from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ3 : TypeAlias = "Response"
"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations
from enum import Enum
import os
from typing import Any, Optional, List, Dict, Union
from dataclasses import dataclass

from quart import jsonify, Response
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from wechaty.config import config


@dataclass
class __typ4:
    """nav metadata"""
    view_url: Optional[str] = None
    author: Optional[str] = None    # name of author
    avatar: Optional[str] = None    # avatar of author
    author_link: Optional[str] = None    # introduction link of author
    icon: Optional[str] = None    # avatar of author


@dataclass
class __typ0:
    """the data transfer object of plugin list"""
    __tmp11: str                       # name of plugin
    status: int                     # status of plugin: 0 / 1

    view_url: Optional[str] = None
    author: Optional[str] = None    # name of author
    avatar: Optional[str] = None    # avatar of author
    author_link: Optional[str] = None    # introduction link of author
    icon: Optional[str] = None    # avatar of author

    def __tmp4(__tmp1, __tmp8: __typ4) :
        """update the field with nav data
        """
        __tmp1.author = __tmp8.author
        __tmp1.author_link = __tmp8.author_link
        __tmp1.avatar = __tmp8.avatar
        __tmp1.icon = __tmp8.icon
        __tmp1.view_url = __tmp8.view_url


def __tmp10(data: __typ2) -> __typ3:
    """make the success response with data

    Args:
        data (dict): the data of response
    """
    return jsonify(dict(
        code=200,
        data=data
    ))


def __tmp6(__tmp7: str) -> __typ3:
    """make the error response with msg

    Args:
        msg (str): the error msg string of data
    """
    return jsonify(dict(
        code=500,
        __tmp7=__tmp7
    ))


@dataclass
class __typ1:
    """options for wechaty plugin"""
    __tmp11: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class WechatySchedulerOptions:
    """options for wechaty scheduler"""
    job_store: Union[str, SQLAlchemyJobStore] = f'sqlite:///{config.cache_dir}/job.db'
    job_store_alias: str = 'wechaty-scheduler'


class __typ5(Enum):
    """plugin running status"""
    Running = 0
    Stopped = 1


class __typ6:
    """cache the static file to avoid time-consuming finding and loading
    """
    def __tmp5(__tmp1, cache_dirs: Optional[List[str]] = None) -> None:
        __tmp1.file_maps: Dict[str, str] = {}

        __tmp1.cache_dirs = cache_dirs or []

    def __tmp2(__tmp1, __tmp3) -> None:
        """add the static file dir

        Args:
            static_file_dir (str): the path of the static file
        """
        if not __tmp3:
            return
        __tmp1.cache_dirs.append(__tmp3)

    def _find_file_path_recursive(__tmp1, __tmp0: str, __tmp11: <FILL>) -> Optional[str]:
        """find the file based on the file-name which will & should be union

        Args:
            base_dir (str): the root dir of static files for the plugin
            name (str): the union name of static file

        Returns:
            Optional[str]: the target static file path
        """
        if not os.path.exists(__tmp0) or os.path.isfile(__tmp0):
            return None

        for file_name in os.listdir(__tmp0):
            if file_name == __tmp11:
                return os.path.join(__tmp0, file_name)
            file_path = os.path.join(__tmp0, file_name)

            target_path = __tmp1._find_file_path_recursive(file_path, __tmp11)
            if target_path:
                return target_path

        return None

    def __tmp9(__tmp1, __tmp11: str) -> Optional[str]:
        """find the file based on the file-name which will & should be union

        Args:
            name (str): the union name of static file

        Returns:
            Optional[str]: the path of the static file
        """
        if __tmp11 in __tmp1.file_maps:
            return __tmp1.file_maps[__tmp11]

        for cache_dir in __tmp1.cache_dirs:
            file_path = __tmp1._find_file_path_recursive(cache_dir, __tmp11)
            if file_path:
                return file_path
        return None
