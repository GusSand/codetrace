from typing import TypeAlias
__typ1 : TypeAlias = "BinaryIO"
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

    def __init__(__tmp0, status_code: __typ0):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ5(__typ2):
    """Page can not be deleted."""


class __typ3(__typ2):
    """Page can not be edited because it is protected."""


class __typ4(__typ2):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data: object):
        """Initialize."""
        __tmp0.data = data
        super().__init__(str(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp0) -> Iterable[__typ0]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp13(
        __tmp0, __tmp15, __tmp11: __typ0, __tmp17,
        __tmp19, __tmp6,
    ) -> Iterator[Dict[str, object]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp4(__tmp0, __tmp11) -> Iterator[Dict[str, str]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp0, image_ids_limit, __tmp9: List[__typ0]
    ) -> Iterator[Dict[str, str]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp0, category_name, __tmp11: __typ0,
        __tmp15: Optional[__typ0] = None, member_type: Optional[str] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp15, __tmp11: __typ0, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) -> Iterator[str]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp14: str,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp8(
        __tmp0, search_request: str, __tmp15: __typ0, __tmp11,
    ) -> Iterator[str]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp15: __typ0, __tmp11: __typ0
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp16(
        __tmp0, file_name: <FILL>, __tmp7, mime_type: Optional[str],
        __tmp5: Optional[str] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp10(
        __tmp0, page_name: str, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, page_name: str, __tmp5, summary: Optional[str] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp0, __tmp14, __tmp15: Optional[__typ0], __tmp11: __typ0
    ) -> Iterator[Dict[str, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, __tmp12, __tmp18: str) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
