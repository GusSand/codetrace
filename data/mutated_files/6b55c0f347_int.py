from typing import TypeAlias
__typ7 : TypeAlias = "BinaryIO"
__typ5 : TypeAlias = "object"
__typ1 : TypeAlias = "str"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class MediaWikiAPIError(click.ClickException):
    """MediaWiki API error."""


class __typ4(MediaWikiAPIError):
    """Status code is not 200."""

    status_code: int

    def __init__(__tmp0, status_code: int):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ0(MediaWikiAPIError):
    """Page can not be deleted."""


class __typ2(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class __typ6(MediaWikiAPIError):
    """MediaWiki API error."""

    data: __typ5

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ1(data))


class __typ3(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp28(__tmp0) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp17(
        __tmp0, __tmp19: int, __tmp14, __tmp27,
        __tmp30: datetime.datetime, __tmp9,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(__tmp0, __tmp14: int) :
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp4(
        __tmp0, __tmp6: int, __tmp12
    ) -> Iterator[Dict[__typ1, __typ1]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp16(
        __tmp0, __tmp21, __tmp14: int,
        __tmp19: Optional[int] = None, member_type: Optional[__typ1] = None
    ) -> Iterator[Dict[__typ1, __typ5]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp19, __tmp14: int, first_page: Optional[__typ1] = None,
        redirect_filter_mode: __typ1 = 'all'
    ) -> Iterator[__typ1]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp18: __typ1,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp11(
        __tmp0, __tmp24, __tmp19, __tmp14,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp19: <FILL>, __tmp14
    ) -> Iterator[Dict[__typ1, __typ5]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp26(
        __tmp0, __tmp25: __typ1, __tmp10, __tmp23: Optional[__typ1],
        __tmp7: Optional[__typ1] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp13(
        __tmp0, __tmp20: __typ1, reason: Optional[__typ1] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp22(
        __tmp0, __tmp20, __tmp7, summary: Optional[__typ1] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp8(
        __tmp0, __tmp18: __typ1, __tmp19: Optional[int], __tmp14
    ) :
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, __tmp15: __typ1, __tmp29) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
