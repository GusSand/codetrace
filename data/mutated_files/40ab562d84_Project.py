"""This module contains operations related to creating gerrit patchset."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import FromVirtualenv
from pipwatch_worker.worker.operations.operation import Operation


class __typ0(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating git-review and submitting it."""

    def __init__(__tmp0, logger, project_details: <FILL>) :
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        __tmp0.from_venv = FromVirtualenv(project_id=__tmp0.project_details.id)

    def __tmp1(__tmp0) -> None:
        """Create gerrit patchset and submit it."""
        __tmp0.log.debug("Attempting to run 'git-review' command..")
        __tmp0.from_venv(
            command="git-review"
        )
