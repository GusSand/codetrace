from typing import TypeAlias
__typ1 : TypeAlias = "Image"
__typ0 : TypeAlias = "FileBox"
"""
Python Wechaty - https://github.com/wechaty/python-wechaty
2020-now @ Copyright Wechaty

GitHub:
    TypeScript: https://github.com/wechaty/wechaty/blob/master/src/user/image.ts
    Python:     https://github.com/wechaty/python-wechaty/blob/master/src/wechaty/user/images.py

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from typing import (
    Type,
)


from wechaty_puppet import (
    FileBox, ImageType, get_logger
)

from ..accessory import Accessory

log = get_logger('Image')


class __typ1(Accessory):
    """
    User Image class
    """

    def __tmp5(__tmp0) :
        return 'Image<%s>' % __tmp0.image_id

    def __init__(
            __tmp0,
            image_id: <FILL>,
    ) :
        """
        :param image_id:
        """
        super().__init__()
        log.info('init the message Image object <%s>', image_id)

        __tmp0.image_id = image_id

    @classmethod
    def __tmp6(__tmp3, image_id) -> __typ1:
        """
        create image instance by image_id
        :param cls:
        :param image_id:
        :return:
        """
        log.info('@classmethod create(%s)', image_id)
        return __tmp3(image_id)

    async def __tmp1(__tmp0) -> __typ0:
        """
        docstring
        :return:
        """
        log.info('thumbnail() for <%s>', __tmp0.image_id)
        image_file = await __tmp0.puppet.message_image(
            message_id=__tmp0.image_id, image_type=ImageType.IMAGE_TYPE_HD)
        return image_file

    async def __tmp2(__tmp0) -> __typ0:
        """
        docstring
        :return:
        """
        log.info('hd() for <%s>', __tmp0.image_id)
        image_file = await __tmp0.puppet.message_image(
            message_id=__tmp0.image_id, image_type=ImageType.IMAGE_TYPE_HD)
        return image_file

    async def __tmp4(__tmp0) :
        """
        docstring
        :return:
        """
        log.info('artwork() for <%s>', __tmp0.image_id)
        image_file = await __tmp0.puppet.message_image(
            message_id=__tmp0.image_id, image_type=ImageType.IMAGE_TYPE_ARTWORK)
        return image_file
