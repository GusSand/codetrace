from typing import TypeAlias
__typ1 : TypeAlias = "str"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class __typ0(click.ClickException):
    """MediaWiki API error."""


class StatusCodeError(__typ0):
    """Status code is not 200."""

    status_code: int

    def __init__(__tmp2, status_code: int):
        """Initialize."""
        __tmp2.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class CanNotDelete(__typ0):
    """Page can not be deleted."""


class PageProtected(__typ0):
    """Page can not be edited because it is protected."""


class MediaWikiAPIMiscError(__typ0):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp2, data: object):
        """Initialize."""
        __tmp2.data = data
        super().__init__(__typ1(data))


class __typ2(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp2) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp6(
        __tmp2, __tmp9: int, __tmp5, user: __typ1,
        __tmp10: datetime.datetime, end_date,
    ) -> Iterator[Dict[__typ1, object]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp0(__tmp2, __tmp5: int) -> Iterator[Dict[__typ1, __typ1]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp2, image_ids_limit: int, page_ids
    ) -> Iterator[Dict[__typ1, __typ1]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp2, category_name: __typ1, __tmp5: int,
        __tmp9: Optional[int] = None, member_type: Optional[__typ1] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp11(
        __tmp2, __tmp9, __tmp5: <FILL>, first_page: Optional[__typ1] = None,
        redirect_filter_mode: __typ1 = 'all'
    ) -> Iterator[__typ1]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp7(
        __tmp2, __tmp8: __typ1,
    ) -> __typ1:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def search_pages(
        __tmp2, __tmp1: __typ1, __tmp9, __tmp5: int,
    ) -> Iterator[__typ1]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp2, __tmp9: int, __tmp5: int
    ) -> Iterator[Dict[__typ1, object]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp4(
        __tmp2, file_name: __typ1, file: BinaryIO, mime_type: Optional[__typ1],
        text: Optional[__typ1] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp2, page_name: __typ1, reason: Optional[__typ1] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp2, page_name, text, summary: Optional[__typ1] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(
        __tmp2, __tmp8, __tmp9: Optional[int], __tmp5
    ) -> Iterator[Dict[__typ1, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp2, username, password: __typ1) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
