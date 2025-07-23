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


class __typ2(MediaWikiAPIError):
    """Page can not be deleted."""


class PageProtected(MediaWikiAPIError):
    """Page can not be edited because it is protected."""


class __typ1(MediaWikiAPIError):
    """MediaWiki API error."""

    data: object

    def __init__(__tmp0, data):
        """Initialize."""
        __tmp0.data = data
        super().__init__(str(data))


class __typ0(ABC):
    """Base MediaWiki API class."""

    @abstractmethod
    def get_namespace_list(__tmp0) :
        """Get iterable of all namespaces in wiki."""
        raise NotImplementedError()

    @abstractmethod
    def get_user_contributions_list(
        __tmp0, __tmp14, __tmp12, __tmp20,
        __tmp22, __tmp8,
    ) :
        """
        Iterate over user edits.

        Iterate over all edits made by `user in `namespace` since `start_date`
        until `end_date`.
        """
        raise NotImplementedError()

    @abstractmethod
    def __tmp5(__tmp0, __tmp12) :
        """
        Iterate over all images in wiki.

        Each image data is dictionary with two fields: `title` and `url`.
        """
        raise NotImplementedError()

    def __tmp4(
        __tmp0, image_ids_limit, __tmp10
    ) :
        """Iterate over images with given page IDs."""
        raise NotImplementedError()

    @abstractmethod
    def get_category_members(
        __tmp0, __tmp16, __tmp12,
        __tmp14: Optional[int] = None, member_type: Optional[str] = None
    ) :
        """Iterate over pages in category `category_name`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp2(
        __tmp0, __tmp14, __tmp12, first_page: Optional[str] = None,
        redirect_filter_mode: str = 'all'
    ) :
        """Iterate over all page names in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp1(
        __tmp0, __tmp13,
    ) :
        """Get text of page with `title`."""
        raise NotImplementedError()

    @abstractmethod
    def search_pages(
        __tmp0, __tmp18, __tmp14, __tmp12,
    ) :
        """Search pages in wiki in `namespace` with `search_request`."""
        raise NotImplementedError()

    @abstractmethod
    def get_deletedrevs_list(
        __tmp0, __tmp14, __tmp12
    ) :
        """Iterate over deleted revisions in wiki in `namespace`."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp19(
        __tmp0, file_name, __tmp9, __tmp17,
        __tmp6: Optional[str] = None, ignore_warnings: bool = True
    ) :
        """Upload file."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp11(
        __tmp0, __tmp15, reason: Optional[str] = None
    ) :
        """Delete page."""
        raise NotImplementedError()

    @abstractmethod
    def edit_page(
        __tmp0, __tmp15, __tmp6, summary: Optional[str] = None
    ) :
        """Edit page, setting new text."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp7(
        __tmp0, __tmp13: <FILL>, __tmp14, __tmp12
    ) :
        """Get list of pages which has links to given page."""
        raise NotImplementedError()

    @abstractmethod
    def __tmp3(__tmp0, username, __tmp21) :
        """Log in to MediaWiki API."""
        raise NotImplementedError()
