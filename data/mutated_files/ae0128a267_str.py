from typing import TypeAlias
__typ2 : TypeAlias = "object"
__typ0 : TypeAlias = "int"
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

    status_code: __typ0

    def __init__(__tmp1, status_code: __typ0):
        """Initialize."""
        __tmp1.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ1(MediaWikiAPIError):
    """Page can not be deleted."""


class PageProtected(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class MediaWikiAPIMiscError(MediaWikiAPIError):
    """MediaWiki API error."""

    data: __typ2

    def __init__(__tmp1, data: __typ2):
        """Initialize."""
        __tmp1.data = data
        super().__init__(str(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp1) -> Iterable[__typ0]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp6(
        __tmp1, __tmp7: __typ0, __tmp4: __typ0, __tmp5,
        start_date: datetime.datetime, end_date: datetime.datetime,
    ) -> Iterator[Dict[str, __typ2]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp0(__tmp1, __tmp4: __typ0) -> Iterator[Dict[str, str]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp1, image_ids_limit, __tmp3
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp1, category_name: <FILL>, __tmp4,
        __tmp7: Optional[__typ0] = None, member_type: Optional[str] = None
    ) -> Iterator[Dict[str, __typ2]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp1, __tmp7: __typ0, __tmp4: __typ0, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) -> Iterator[str]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page(
        __tmp1, title,
    ) -> str:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def search_pages(
        __tmp1, search_request, __tmp7, __tmp4,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp1, __tmp7, __tmp4: __typ0
    ) -> Iterator[Dict[str, __typ2]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp1, file_name: str, file: BinaryIO, mime_type,
        text: Optional[str] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp1, __tmp8: str, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp1, __tmp8: str, text, summary: Optional[str] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp1, title: str, __tmp7, __tmp4
    ) :
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp1, username, password) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
