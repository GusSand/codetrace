from typing import TypeAlias
__typ0 : TypeAlias = "Project"
"""This module contains operations related to cloning project."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git
from pipwatch_worker.worker.operations.operation import Operation


class Clone(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of cloning given project (and keeping it up to date)."""

    def __init__(__tmp0, logger: <FILL>, project_details: __typ0) -> None:
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        __tmp0.git = Git(
            project_id=__tmp0.project_details.id,
            project_url=__tmp0.project_details.git_repository.url,
            project_upstream=__tmp0.project_details.git_repository.upstream_url
        )

    def __tmp1(__tmp0) -> None:
        """Clone given repository (or - if it already exists - pull latest changes)."""
        __tmp0.log.debug("Attempting to run 'git reset --hard'")
        __tmp0.git(command="reset --hard HEAD~1")
        __tmp0.log.debug("Attempting to run 'git clean -fd'")
        __tmp0.git(command="clean -fd")
        __tmp0.log.debug("Attempting to run 'git pull'")
        __tmp0.git(command="pull")

        __tmp0._handle_upstream_sync()

    def _handle_upstream_sync(__tmp0) :
        """Synchronize fork with upstream repository."""
        if not __tmp0.project_details.git_repository.upstream_url:
            return

        __tmp0.git(command="fetch upstream")
        __tmp0.git(command="merge upstream/master")
