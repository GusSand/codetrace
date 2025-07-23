from typing import TypeAlias
__typ1 : TypeAlias = "BinaryIO"
__typ5 : TypeAlias = "object"
__typ0 : TypeAlias = "int"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class __typ2(click.ClickException):
    """MediaWiki API error."""


class StatusCodeError(__typ2):
    """Status code is not 200."""

    status_code: __typ0

    def __init__(__tmp0, status_code):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ7(__typ2):
    """Page can not be deleted."""


class __typ3(__typ2):
    """Page can not be edited because it is protected."""


class __typ6(__typ2):
    """MediaWiki API error."""

    data: __typ5

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(str(data))


class __typ4(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp22(__tmp0) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp0, __tmp17: __typ0, __tmp13: __typ0, __tmp21: str,
        __tmp24, __tmp9: datetime.datetime,
    ) -> Iterator[Dict[str, __typ5]]:
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
        __tmp0, __tmp5: __typ0, page_ids
    ) -> Iterator[Dict[str, str]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp14(
        __tmp0, category_name: str, __tmp13,
        __tmp17: Optional[__typ0] = None, member_type: Optional[str] = None
    ) -> Iterator[Dict[str, __typ5]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp0, __tmp17: __typ0, __tmp13, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) :
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp15,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp11(
        __tmp0, __tmp20, __tmp17, __tmp13: __typ0,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(
        __tmp0, __tmp17: __typ0, __tmp13
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp0, file_name, __tmp10: __typ1, __tmp19,
        __tmp7: Optional[str] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp16: str, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp18(
        __tmp0, __tmp16, __tmp7, summary: Optional[str] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp8(
        __tmp0, __tmp15: str, __tmp17, __tmp13: __typ0
    ) :
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(__tmp0, username: <FILL>, __tmp23: str) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
