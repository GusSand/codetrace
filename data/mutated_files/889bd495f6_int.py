from typing import TypeAlias
__typ6 : TypeAlias = "object"
__typ8 : TypeAlias = "BinaryIO"
__typ2 : TypeAlias = "str"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class __typ1(click.ClickException):
    """MediaWiki API error."""


class __typ5(__typ1):
    """Status code is not 200."""

    status_code: int

    def __init__(__tmp0, status_code):
        """Initialize."""
        __tmp0.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ0(__typ1):
    """Page can not be deleted."""


class __typ3(__typ1):
    """Page can not be edited because it is protected."""


class __typ7(__typ1):
    """MediaWiki API error."""

    data: __typ6

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(__typ2(data))


class __typ4(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp0) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp0, __tmp6: int, __tmp2, user: __typ2,
        __tmp7, __tmp8,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp0, __tmp2: <FILL>) -> Iterator[Dict[__typ2, __typ2]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp0, image_ids_limit, page_ids
    ) -> Iterator[Dict[__typ2, __typ2]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp0, category_name, __tmp2,
        __tmp6: Optional[int] = None, member_type: Optional[__typ2] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp0, __tmp6, __tmp2, first_page: Optional[__typ2] = None,
        redirect_filter_mode: __typ2 = 'all'
    ) -> Iterator[__typ2]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page(
        __tmp0, __tmp5: __typ2,
    ) -> __typ2:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def search_pages(
        __tmp0, search_request, __tmp6, __tmp2,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp6, __tmp2
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp0, __tmp1, file, mime_type: Optional[__typ2],
        text: Optional[__typ2] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp0, page_name: __typ2, reason: Optional[__typ2] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, page_name, text, summary: Optional[__typ2] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp0, __tmp5, __tmp6: Optional[int], __tmp2: int
    ) -> Iterator[Dict[__typ2, __typ6]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp0, __tmp3, __tmp4: __typ2) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
