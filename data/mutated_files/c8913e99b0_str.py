from typing import TypeAlias
__typ6 : TypeAlias = "object"
__typ8 : TypeAlias = "BinaryIO"
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

    def __init__(__tmp1, status_code: __typ0):
        """Initialize."""
        __tmp1.status_code = status_code
        super().__init__(f'Status code is {status_code}')


class __typ1(__typ2):
    """Page can not be deleted."""


class __typ3(__typ2):
    """Page can not be edited because it is protected."""


class __typ7(__typ2):
    """MediaWiki API error."""

    data: __typ6

    def __init__(__tmp1, data: __typ6):
        """Initialize."""
        __tmp1.data = data
        super().__init__(str(data))


class __typ4(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp1) -> Iterable[__typ0]:
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp1, namespace, __tmp3: __typ0, user: str,
        start_date: datetime.datetime, end_date: datetime.datetime,
    ) -> Iterator[Dict[str, __typ6]]:
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_image_list(__tmp1, __tmp3) -> Iterator[Dict[str, str]]:
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def get_page_image_list(
        __tmp1, __tmp0: __typ0, page_ids
    ) -> Iterator[Dict[str, str]]:
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp1, category_name: str, __tmp3,
        namespace: Optional[__typ0] = None, member_type: Optional[str] = None
    ) -> Iterator[Dict[str, __typ6]]:
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def get_page_list(
        __tmp1, namespace: __typ0, __tmp3, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) -> Iterator[str]:
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp4(
        __tmp1, title: str,
    ) -> str:
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp7(
        __tmp1, search_request: str, namespace: __typ0, __tmp3: __typ0,
    ) -> Iterator[str]:
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp1, namespace: __typ0, __tmp3: __typ0
    ) -> Iterator[Dict[str, __typ6]]:
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def upload_file(
        __tmp1, file_name: str, __tmp6: __typ8, mime_type,
        text: Optional[str] = None, ignore_warnings: bool = True
    ) -> None:
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def delete_page(
        __tmp1, page_name: str, reason: Optional[str] = None
    ) -> None:
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(
        __tmp1, page_name: str, text, summary: Optional[str] = None
    ) -> None:
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def get_backlinks(
        __tmp1, title: str, namespace: Optional[__typ0], __tmp3: __typ0
    ) -> Iterator[Dict[str, __typ6]]:
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def api_login(__tmp1, __tmp2: str, password: <FILL>) -> None:
        """Log in to MediaWiki API."""
        raise NotImplementedError()
