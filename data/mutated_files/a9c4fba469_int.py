from typing import TypeAlias
__typ4 : TypeAlias = "object"
__typ0 : TypeAlias = "BinaryIO"
__typ2 : TypeAlias = "str"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class __typ1(click.ClickException):
    """MediaWiki API error."""


class StatusCodeError(__typ1):
    """Status code is not 200."""

    status_code: int

    def __init__(__tmp0, status_code: int):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ6(__typ1):
    """Page can not be deleted."""


class __typ3(__typ1):
    """Page can not be edited because it is protected."""


class __typ5(__typ1):
    """MediaWiki API error."""

    data: __typ4

    def __init__(__tmp0, data: __typ4):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ2(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp23(__tmp0) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp16(
        __tmp0, __tmp18: <FILL>, __tmp14: int, __tmp22: __typ2,
        __tmp24: datetime.datetime, __tmp8: datetime.datetime,
    ) -> Iterator[Dict[__typ2, __typ4]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(__tmp0, __tmp14: int) -> Iterator[Dict[__typ2, __typ2]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp0, __tmp6: int, __tmp11: List[int]
    ) -> Iterator[Dict[__typ2, __typ2]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp15(
        __tmp0, category_name: __typ2, __tmp14: int,
        __tmp18: Optional[int] = None, member_type: Optional[__typ2] = None
    ) -> Iterator[Dict[__typ2, __typ4]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp18: int, __tmp14: int, first_page: Optional[__typ2] = None,
        redirect_filter_mode: __typ2 = 'all'
    ) -> Iterator[__typ2]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp17: __typ2,
    ) -> __typ2:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp10(
        __tmp0, __tmp20: __typ2, __tmp18: int, __tmp14: int,
    ) -> Iterator[__typ2]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp4(
        __tmp0, __tmp18: int, __tmp14: int
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp21(
        __tmp0, file_name: __typ2, __tmp9, mime_type: Optional[__typ2],
        __tmp7: Optional[__typ2] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp19: __typ2, reason: Optional[__typ2] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, __tmp19: __typ2, __tmp7: __typ2, summary: Optional[__typ2] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp0, __tmp17: __typ2, __tmp18: Optional[int], __tmp14
    ) -> Iterator[Dict[__typ2, __typ4]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, __tmp13, password) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
