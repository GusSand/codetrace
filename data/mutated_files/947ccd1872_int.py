from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "object"
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

    def __init__(__tmp3, status_code: <FILL>):
        """Initialize."""
        __tmp3.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class CanNotDelete(__typ0):
    """Page can not be deleted."""


class PageProtected(__typ0):
    """Page can not be edited because it is protected."""


class __typ1(__typ0):
    """MediaWiki API error."""

    data: __typ3

    def __init__(__tmp3, data):
        """Initialize."""
        __tmp3.data = data
        super().__init__(__typ2(data))


class MediaWikiAPI(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp3) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp3, __tmp10, __tmp6, user: __typ2,
        __tmp12, end_date: datetime.datetime,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp0(__tmp3, __tmp6) -> Iterator[Dict[__typ2, __typ2]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp4(
        __tmp3, image_ids_limit, page_ids
    ) -> Iterator[Dict[__typ2, __typ2]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp3, __tmp11, __tmp6: int,
        __tmp10: Optional[int] = None, member_type: Optional[__typ2] = None
    ) -> Iterator[Dict[__typ2, __typ3]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp3, __tmp10, __tmp6, first_page: Optional[__typ2] = None,
        redirect_filter_mode: __typ2 = 'all'
    ) :
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp8(
        __tmp3, __tmp9,
    ) -> __typ2:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def search_pages(
        __tmp3, search_request: __typ2, __tmp10: int, __tmp6: int,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp3, __tmp10, __tmp6: int
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp3, file_name: __typ2, __tmp13: BinaryIO, __tmp14,
        __tmp1: Optional[__typ2] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp3, page_name, reason: Optional[__typ2] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp3, page_name, __tmp1: __typ2, summary: Optional[__typ2] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp3, __tmp9, __tmp10, __tmp6: int
    ) -> Iterator[Dict[__typ2, __typ3]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp3, __tmp7, password) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
