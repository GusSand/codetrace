from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

    def __init__(__tmp0, status_code: int):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class CanNotDelete(MediaWikiAPIError):
    """Page can not be deleted."""


class PageProtected(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class MediaWikiAPIMiscError(MediaWikiAPIError):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data: object):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ0(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp0) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp17(
        __tmp0, __tmp19, __tmp15: int, __tmp27: __typ0,
        start_date: datetime.datetime, __tmp10,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp6(__tmp0, __tmp15) -> Iterator[Dict[__typ0, __typ0]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp4(
        __tmp0, __tmp7: int, __tmp13
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp16(
        __tmp0, __tmp21: __typ0, __tmp15: int,
        __tmp19: Optional[int] = None, member_type: Optional[__typ0] = None
    ) -> Iterator[Dict[__typ0, object]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp19: <FILL>, __tmp15: int, first_page: Optional[__typ0] = None,
        redirect_filter_mode: __typ0 = 'all'
    ) -> Iterator[__typ0]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp18: __typ0,
    ) -> __typ0:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp24: __typ0, __tmp19: int, __tmp15: int,
    ) -> Iterator[__typ0]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp0, __tmp19, __tmp15: int
    ) -> Iterator[Dict[__typ0, object]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp26(
        __tmp0, __tmp25, __tmp11: BinaryIO, __tmp23: Optional[__typ0],
        __tmp8: Optional[__typ0] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp14(
        __tmp0, __tmp20: __typ0, reason: Optional[__typ0] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp22(
        __tmp0, __tmp20, __tmp8: __typ0, summary: Optional[__typ0] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp9(
        __tmp0, __tmp18: __typ0, __tmp19: Optional[int], __tmp15
    ) -> Iterator[Dict[__typ0, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, username: __typ0, __tmp28) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
