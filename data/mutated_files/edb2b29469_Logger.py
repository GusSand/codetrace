"""This module contains operations related to creating gerrit patchset."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import FromVirtualenv
from pipwatch_worker.worker.operations.operation import Operation


class GitReview(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating git-review and submitting it."""

    def __init__(__tmp1, __tmp0: <FILL>, project_details) -> None:
        """Create method instance."""
        super().__init__(__tmp0=__tmp0, project_details=project_details)
        __tmp1.from_venv = FromVirtualenv(project_id=__tmp1.project_details.id)

    def __tmp2(__tmp1) -> None:
        """Create gerrit patchset and submit it."""
        __tmp1.log.debug("Attempting to run 'git-review' command..")
        __tmp1.from_venv(
            command="git-review"
        )
