from typing import TypeAlias
__typ2 : TypeAlias = "object"
__typ0 : TypeAlias = "str"
__typ4 : TypeAlias = "BinaryIO"
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


class CanNotDelete(MediaWikiAPIError):
    """Page can not be deleted."""


class PageProtected(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class __typ3(MediaWikiAPIError):
    """MediaWiki API error."""

    data: __typ2

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ0(data))


class __typ1(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp0) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp14, __tmp10, __tmp21: __typ0,
        __tmp23: datetime.datetime, end_date,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp0, __tmp10: int) :
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp3(
        __tmp0, image_ids_limit: int, __tmp8
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp0, __tmp16: __typ0, __tmp10,
        __tmp14: Optional[int] = None, member_type: Optional[__typ0] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp0, __tmp14: int, __tmp10: int, first_page: Optional[__typ0] = None,
        redirect_filter_mode: __typ0 = 'all'
    ) -> Iterator[__typ0]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp13,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp7(
        __tmp0, __tmp19, __tmp14, __tmp10,
    ) -> Iterator[__typ0]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp14, __tmp10: int
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp0, __tmp20: __typ0, __tmp6: __typ4, __tmp18: Optional[__typ0],
        __tmp4: Optional[__typ0] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp9(
        __tmp0, __tmp15: __typ0, reason: Optional[__typ0] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp17(
        __tmp0, __tmp15: __typ0, __tmp4: __typ0, summary: Optional[__typ0] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp0, __tmp13: __typ0, __tmp14, __tmp10: <FILL>
    ) -> Iterator[Dict[__typ0, __typ2]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(__tmp0, __tmp11: __typ0, __tmp22) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
