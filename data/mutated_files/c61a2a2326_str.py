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


class __typ0(MediaWikiAPIError):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(str(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp7(__tmp0) -> Iterable[int]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp6(
        __tmp0, __tmp10, __tmp4, user: str,
        __tmp11: datetime.datetime, end_date,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp0, __tmp4) -> Iterator[Dict[str, str]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp14(
        __tmp0, image_ids_limit, __tmp2: List[int]
    ) -> Iterator[Dict[str, str]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp0, category_name, __tmp4,
        __tmp10: Optional[int] = None, member_type: Optional[str] = None
    ) -> Iterator[Dict[str, object]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, __tmp10: int, __tmp4, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) -> Iterator[str]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page(
        __tmp0, __tmp9: str,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp13(
        __tmp0, search_request, __tmp10, __tmp4,
    ) -> Iterator[str]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp10, __tmp4
    ) -> Iterator[Dict[str, object]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp0, file_name, file, mime_type: Optional[str],
        __tmp1: Optional[str] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(
        __tmp0, page_name, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, page_name: str, __tmp1: <FILL>, summary: Optional[str] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp0, __tmp9, __tmp10, __tmp4
    ) -> Iterator[Dict[str, object]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp0, username, __tmp8: str) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
