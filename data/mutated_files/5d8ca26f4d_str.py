from typing import TypeAlias
__typ5 : TypeAlias = "object"
__typ0 : TypeAlias = "int"
"""MediaWiki API interaction functions."""
import datetime
from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Iterable, Iterator, List, Optional

import click

NAMESPACE_IMAGES = 6


class __typ1(click.ClickException):
    """MediaWiki API error."""


class __typ4(__typ1):
    """Status code is not 200."""

    status_code: __typ0

    def __init__(__tmp1, status_code: __typ0):
        """Initialize."""
        __tmp1.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class CanNotDelete(__typ1):
    """Page can not be deleted."""


class __typ2(__typ1):
    """Page can not be edited because it is protected."""


class __typ6(__typ1):
    """MediaWiki API error."""

    data: __typ5

    def __init__(__tmp1, data: __typ5):
        """Initialize."""
        __tmp1.data = data
        super().__init__(str(data))


class __typ3(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp1) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp1, __tmp9: __typ0, __tmp6: __typ0, user: str,
        __tmp5: datetime.datetime, end_date: datetime.datetime,
    ) -> Iterator[Dict[str, __typ5]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp0(__tmp1, __tmp6) :
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp2(
        __tmp1, image_ids_limit, page_ids: List[__typ0]
    ) -> Iterator[Dict[str, str]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp1, category_name, __tmp6,
        __tmp9: Optional[__typ0] = None, member_type: Optional[str] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp12(
        __tmp1, __tmp9, __tmp6, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) :
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp11(
        __tmp1, __tmp8: <FILL>,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp14(
        __tmp1, search_request: str, __tmp9, __tmp6: __typ0,
    ) -> Iterator[str]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp1, __tmp9: __typ0, __tmp6: __typ0
    ) -> Iterator[Dict[str, __typ5]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp1, __tmp3: str, file: BinaryIO, __tmp15: Optional[str],
        text: Optional[str] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp4(
        __tmp1, __tmp10, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp1, __tmp10: str, text: str, summary: Optional[str] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp1, __tmp8: str, __tmp9: Optional[__typ0], __tmp6: __typ0
    ) -> Iterator[Dict[str, __typ5]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp13(__tmp1, __tmp7, password) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
