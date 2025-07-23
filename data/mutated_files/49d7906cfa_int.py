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

    def __init__(__tmp0, status_code: int):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class CanNotDelete(MediaWikiAPIError):
    """Page can not be deleted."""


class PageProtected(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class __typ0(MediaWikiAPIError):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data: object):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ1(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp24(__tmp0) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp15(
        __tmp0, __tmp17, __tmp13: int, __tmp23,
        __tmp26, end_date,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp6(__tmp0, __tmp13) :
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp4(
        __tmp0, __tmp7: int, __tmp11
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp14(
        __tmp0, __tmp19, __tmp13: int,
        __tmp17: Optional[int] = None, member_type: Optional[__typ1] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp17, __tmp13, first_page: Optional[__typ1] = None,
        redirect_filter_mode: __typ1 = 'all'
    ) -> Iterator[__typ1]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp16,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp10(
        __tmp0, __tmp21, __tmp17, __tmp13,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp0, __tmp17: int, __tmp13: <FILL>
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp22(
        __tmp0, file_name, file, __tmp20: Optional[__typ1],
        __tmp8: Optional[__typ1] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp0, __tmp18, reason: Optional[__typ1] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, __tmp18: __typ1, __tmp8: __typ1, summary: Optional[__typ1] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp9(
        __tmp0, __tmp16, __tmp17, __tmp13
    ) -> Iterator[Dict[__typ1, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, __tmp12, __tmp25: __typ1) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
