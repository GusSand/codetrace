from typing import TypeAlias
__typ1 : TypeAlias = "Project"
"""This module contains operations related to pushing git changes."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git
from pipwatch_worker.worker.operations.operation import Operation


class __typ0(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of pushing git changes up to parent repository."""

    def __init__(__tmp0, logger: <FILL>, project_details) :
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        __tmp0.git = Git(__tmp0.project_details.id, __tmp0.project_details.git_repository.url)

    def __tmp1(__tmp0) :
        """Push git changes."""
        __tmp0.log.debug("Attempting to run 'git push' command..")
        __tmp0.git("push")
