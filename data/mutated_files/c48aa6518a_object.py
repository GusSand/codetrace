from typing import TypeAlias
__typ8 : TypeAlias = "BinaryIO"
__typ3 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class __typ2(click.ClickException):
    """MediaWiki API error."""


class __typ6(__typ2):
    """Status code is not 200."""

    status_code: __typ0

    def __init__(__tmp1, status_code: __typ0):
        """Initialize."""
        __tmp1.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ1(__typ2):
    """Page can not be deleted."""


class __typ4(__typ2):
    """Page can not be edited because it is protected."""


class __typ7(__typ2):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp1, data: <FILL>):
        """Initialize."""
        __tmp1.data = data
        super().__init__(__typ3(data))


class __typ5(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp1) -> Iterable[__typ0]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp1, __tmp7: __typ0, __tmp6: __typ0, user: __typ3,
        start_date: datetime.datetime, end_date,
    ) -> Iterator[Dict[__typ3, object]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp1, __tmp6: __typ0) -> Iterator[Dict[__typ3, __typ3]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp2(
        __tmp1, image_ids_limit: __typ0, __tmp4
    ) -> Iterator[Dict[__typ3, __typ3]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp1, __tmp9: __typ3, __tmp6: __typ0,
        __tmp7: Optional[__typ0] = None, member_type: Optional[__typ3] = None
    ) -> Iterator[Dict[__typ3, object]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp1, __tmp7: __typ0, __tmp6, first_page: Optional[__typ3] = None,
        redirect_filter_mode: __typ3 = 'all'
    ) -> Iterator[__typ3]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page(
        __tmp1, title: __typ3,
    ) -> __typ3:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def search_pages(
        __tmp1, __tmp0: __typ3, __tmp7: __typ0, __tmp6: __typ0,
    ) -> Iterator[__typ3]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp10(
        __tmp1, __tmp7: __typ0, __tmp6: __typ0
    ) -> Iterator[Dict[__typ3, object]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(
        __tmp1, file_name, file: __typ8, mime_type: Optional[__typ3],
        text: Optional[__typ3] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp1, __tmp8: __typ3, reason: Optional[__typ3] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp1, __tmp8: __typ3, text: __typ3, summary: Optional[__typ3] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp1, title, __tmp7: Optional[__typ0], __tmp6: __typ0
    ) -> Iterator[Dict[__typ3, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp1, username, password: __typ3) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
