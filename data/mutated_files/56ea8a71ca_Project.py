from typing import TypeAlias
__typ1 : TypeAlias = "Logger"
"""This module contains operations related to pushing git changes."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git
from pipwatch_worker.worker.operations.operation import Operation


class __typ0(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of pushing git changes up to parent repository."""

    def __init__(self, __tmp0, project_details: <FILL>) :
        """Create method instance."""
        super().__init__(__tmp0=__tmp0, project_details=project_details)
        self.git = Git(self.project_details.id, self.project_details.git_repository.url)

    def __tmp1(self) :
        """Push git changes."""
        self.log.debug("Attempting to run 'git push' command..")
        self.git("push")
