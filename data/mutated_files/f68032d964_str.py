from typing import TypeAlias
__typ6 : TypeAlias = "object"
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


class __typ5(__typ2):
    """Status code is not 200."""

    status_code: __typ0

    def __init__(__tmp0, status_code: __typ0):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ7(__typ2):
    """Page can not be deleted."""


class __typ3(__typ2):
    """Page can not be edited because it is protected."""


class MediaWikiAPIMiscError(__typ2):
    """MediaWiki API error."""

    data: __typ6

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(str(data))


class __typ4(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def __tmp6(__tmp0) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp0, __tmp9, __tmp3, __tmp5: str,
        start_date: datetime.datetime, end_date: datetime.datetime,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp0, __tmp3) -> Iterator[Dict[str, str]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp13(
        __tmp0, image_ids_limit: __typ0, page_ids: List[__typ0]
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp0, category_name, __tmp3: __typ0,
        __tmp9: Optional[__typ0] = None, member_type: Optional[str] = None
    ) -> Iterator[Dict[str, __typ6]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp0, __tmp9, __tmp3: __typ0, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) -> Iterator[str]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page(
        __tmp0, __tmp8,
    ) -> str:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp0, search_request: <FILL>, __tmp9, __tmp3,
    ) -> Iterator[str]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp9: __typ0, __tmp3
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp1: str, __tmp11, mime_type: Optional[str],
        text: Optional[str] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp0, __tmp10: str, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, __tmp10: str, text: str, summary: Optional[str] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp0, __tmp8, __tmp9: Optional[__typ0], __tmp3
    ) -> Iterator[Dict[str, __typ6]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp0, __tmp4, __tmp7: str) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
