from typing import TypeAlias
__typ0 : TypeAlias = "Logger"
"""This module contains worker operation interface definition."""
from logging import getLogger, Logger

from pipwatch_worker.worker.commands import RepositoriesCacheMixin
from pipwatch_worker.core.data_models import Project


class __typ1(RepositoriesCacheMixin):  # pylint: disable=too-few-public-methods
    """Defines common interface for different operations that worker may perform on a project."""

    def __init__(
            __tmp1,
            __tmp0,
            project_details: <FILL>
    ) :
        """Create method instance."""
        super().__init__()
        __tmp1.log = __tmp0 or getLogger(__name__)
        __tmp1.project_details = project_details

    def __tmp2(__tmp1) :
        """Run operation (need to be overridden and implemented)."""
        raise NotImplementedError()
