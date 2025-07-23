from typing import TypeAlias
__typ0 : TypeAlias = "Logger"
"""This module contains operations related to cloning project."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git
from pipwatch_worker.worker.operations.operation import Operation


class Clone(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of cloning given project (and keeping it up to date)."""

    def __init__(__tmp1, __tmp0, project_details: <FILL>) -> None:
        """Create method instance."""
        super().__init__(__tmp0=__tmp0, project_details=project_details)
        __tmp1.git = Git(
            project_id=__tmp1.project_details.id,
            project_url=__tmp1.project_details.git_repository.url,
            project_upstream=__tmp1.project_details.git_repository.upstream_url
        )

    def __call__(__tmp1) :
        """Clone given repository (or - if it already exists - pull latest changes)."""
        __tmp1.log.debug("Attempting to run 'git reset --hard'")
        __tmp1.git(command="reset --hard HEAD~1")
        __tmp1.log.debug("Attempting to run 'git clean -fd'")
        __tmp1.git(command="clean -fd")
        __tmp1.log.debug("Attempting to run 'git pull'")
        __tmp1.git(command="pull")

        __tmp1._handle_upstream_sync()

    def _handle_upstream_sync(__tmp1) -> None:
        """Synchronize fork with upstream repository."""
        if not __tmp1.project_details.git_repository.upstream_url:
            return

        __tmp1.git(command="fetch upstream")
        __tmp1.git(command="merge upstream/master")
