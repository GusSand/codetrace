"""ContactSelf"""

from __future__ import annotations
from typing import Any, Optional, Type

from wechaty import FileBox, get_logger
from wechaty.exceptions import WechatyOperationError
from wechaty.user.contact import Contact

log = get_logger('ContactSelf')


class __typ0(Contact):
    """ContactSelf"""

    async def avatar(__tmp1, file_box: Optional[FileBox] = None) :
        """
        Get or set avatar of ContactSelf.

        Args:
            file_box: FileBox object, if not provided, it will return a FileBox object

        Examples:
            >>> contact_self = bot.contact_self()
            >>> file_box = await contact_self.avatar()
            >>> file_box = await contact_self.avatar(file_box)

        Raises:
            WechatyOperationError: if the contact is not self, it will not get the avatar

        Returns:
            FileBox: file_box
        """
        log.info('avatar(%s)' % file_box.name if file_box else '')
        if not file_box:
            file_box = await super().avatar(None)
            return file_box

        if __tmp1.contact_id != __tmp1.puppet.self_id():
            raise WechatyOperationError('set avatar only available for user self')

        await __tmp1.puppet.contact_avatar(__tmp1.contact_id, file_box)

    async def __tmp0(__tmp1) :
        """
        Return the qrcode of ContactSelf
        
        Examples:
            >>> contact_self = bot.contact_self()
            >>> qr_code = await contact_self.qr_code()

        Raises:
            WechatyOperationError: if there is login exception, it will not get the qrcode
            WechatyOperationError: if the contact is not self, it will not get the qrcode

        Returns:
            str: the content of qrcode
        """
        try:
            contact_id: str = __tmp1.puppet.self_id()
        except Exception:
            raise WechatyOperationError(
                'Can not get qr_code, user might be either not logged in or already logged out'
            )

        if __tmp1.contact_id != contact_id:
            raise WechatyOperationError('only can get qr_code for the login user self')
        qr_code_value = await __tmp1.puppet.contact_self_qr_code()
        return qr_code_value

    @property
    def name(__tmp1) :
        """
        Get the name of login contact.

        Examples:
            >>> contact_self = bot.contact_self()
            >>> name = contact_self.name

        Returns:
            str: the name of Login User
        """
        return super().name

    async def __tmp2(__tmp1, name: <FILL>) -> None:
        """
        Set the name of login contact.

        Args:
            name: new name

        Examples:
            >>> contact_self = bot.contact_self()
            >>> await contact_self.set_name('new name')
        """
        await __tmp1.puppet.contact_self_name(name)
        await __tmp1.ready(force_sync=True)

    async def __tmp3(__tmp1, __tmp3: str) -> Any:
        """
        Set the signature of login contact.

        Args:
            signature: new signature

        Examples:
            >>> contact_self = bot.contact_self()
            >>> await contact_self.signature('new signature')
        
        Raises:
            WechatyOperationError: if there is login exception, it will not set the signature
            WechatyOperationError: if the contact is not self, it will not set the signature
        
        Returns:
            Any: the signature of login user
        """
        puppet_id = __tmp1.puppet.self_id()

        if __tmp1.contact_id != puppet_id:
            raise WechatyOperationError('only can get qr_code for the login user self')

        return __tmp1.puppet.contact_signature(__tmp3)
