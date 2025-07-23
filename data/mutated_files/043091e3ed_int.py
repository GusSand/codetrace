from typing import TypeAlias
__typ2 : TypeAlias = "str"
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

    def __init__(__tmp0, status_code):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class CanNotDelete(__typ0):
    """Page can not be deleted."""


class __typ3(__typ0):
    """Page can not be edited because it is protected."""


class __typ1(__typ0):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ2(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp29(__tmp0) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp18(
        __tmp0, __tmp20: int, __tmp15, __tmp28: __typ2,
        __tmp31: datetime.datetime, __tmp10,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp6(__tmp0, __tmp15: int) -> Iterator[Dict[__typ2, __typ2]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp4(
        __tmp0, __tmp7: int, __tmp13: List[int]
    ) -> Iterator[Dict[__typ2, __typ2]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp17(
        __tmp0, __tmp22, __tmp15,
        __tmp20: Optional[int] = None, member_type: Optional[__typ2] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp20, __tmp15: int, first_page: Optional[__typ2] = None,
        redirect_filter_mode: __typ2 = 'all'
    ) :
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp19,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp25, __tmp20, __tmp15: <FILL>,
    ) -> Iterator[__typ2]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp0, __tmp20, __tmp15
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp27(
        __tmp0, __tmp26, __tmp11, __tmp24,
        __tmp8: Optional[__typ2] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp14(
        __tmp0, __tmp21: __typ2, reason: Optional[__typ2] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp23(
        __tmp0, __tmp21, __tmp8: __typ2, summary: Optional[__typ2] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp9(
        __tmp0, __tmp19: __typ2, __tmp20: Optional[int], __tmp15
    ) :
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, __tmp16, __tmp30: __typ2) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
