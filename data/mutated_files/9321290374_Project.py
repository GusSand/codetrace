from typing import TypeAlias
__typ0 : TypeAlias = "Logger"
"""This module contains operations related to committing and reviewing changes done to requirements."""
from logging import Logger

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.commands import Git
from pipwatch_worker.worker.operations.operation import Operation


class CommitChanges(Operation):  # pylint: disable=too-few-public-methods
    """Encompasses logic of committing changes made to requirements."""

    DEFAULT_COMMIT_MSG = "[Pipwatch] - Automatic increment of requirements versions."

    def __init__(__tmp0, logger, project_details: <FILL>) :
        """Initialize method instance."""
        super().__init__(logger=logger, project_details=project_details)
        __tmp0.git = Git(__tmp0.project_details.id, __tmp0.project_details.git_repository.url)

    def __call__(__tmp0, commit_msg: str = None) :
        """Commit changes and push them to master branch."""
        for requirements_file in __tmp0.project_details.requirements_files:
            __tmp0.log.debug("Attempting to 'git add {file}'".format(file=requirements_file.path))
            __tmp0.git("add {file}".format(file=requirements_file.path))

        commit_msg = commit_msg if commit_msg else __tmp0.DEFAULT_COMMIT_MSG
        __tmp0.log.debug("Attempting to commit changes with following message: '{message}'".format(
            message=commit_msg
        ))
        __tmp0.git("commit -m {commit_msg}".format(commit_msg=commit_msg))
