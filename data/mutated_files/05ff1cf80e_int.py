from typing import TypeAlias
__typ1 : TypeAlias = "str"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class MediaWikiAPIError(click.ClickException):
    """MediaWiki API error."""


class StatusCodeError(MediaWikiAPIError):
    """Status code is not 200."""

    status_code: int

    def __init__(__tmp0, status_code):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ2(MediaWikiAPIError):
    """Page can not be deleted."""


class PageProtected(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class MediaWikiAPIMiscError(MediaWikiAPIError):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ1(data))


class __typ0(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp0) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp0, __tmp10, __tmp5: int, __tmp6,
        __tmp4: datetime.datetime, __tmp13: datetime.datetime,
    ) -> Iterator[Dict[__typ1, object]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp0, __tmp5) :
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp0, image_ids_limit: int, __tmp3
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp0, category_name, __tmp5,
        __tmp10: Optional[int] = None, member_type: Optional[__typ1] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp0, __tmp10: int, __tmp5: int, first_page: Optional[__typ1] = None,
        redirect_filter_mode: __typ1 = 'all'
    ) -> Iterator[__typ1]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp9: __typ1,
    ) -> __typ1:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp16(
        __tmp0, search_request, __tmp10: <FILL>, __tmp5: int,
    ) -> Iterator[__typ1]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp17(
        __tmp0, __tmp10, __tmp5: int
    ) -> Iterator[Dict[__typ1, object]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp0, __tmp1: __typ1, file, mime_type: Optional[__typ1],
        text: Optional[__typ1] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp0, __tmp11, reason: Optional[__typ1] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp14(
        __tmp0, __tmp11: __typ1, text, summary: Optional[__typ1] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp9, __tmp10, __tmp5: int
    ) -> Iterator[Dict[__typ1, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp15(__tmp0, __tmp7: __typ1, __tmp8: __typ1) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
