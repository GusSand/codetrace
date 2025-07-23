from typing import TypeAlias
__typ0 : TypeAlias = "bool"
"""This module contains operations related to updating requirements of project."""
from logging import Logger
import os

from pipwatch_worker.core.data_models import Project, RequirementsFile
from pipwatch_worker.core.utils import get_pip_script_name
from pipwatch_worker.worker.commands import Command, FromVirtualenv, Git
from pipwatch_worker.worker.operations.operation import Operation


class __typ1(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of attempt of updating requirements of given project."""

    def __init__(__tmp0, logger: <FILL>, project_details) :
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)

        __tmp0.command = Command(project_id=__tmp0.project_details.id)
        __tmp0.from_venv = FromVirtualenv(project_id=__tmp0.project_details.id)
        __tmp0.git = Git(
            project_id=__tmp0.project_details.id,
            project_url=__tmp0.project_details.git_repository.url
        )

    def __call__(__tmp0) -> None:
        """Update requirements of given project."""
        for requirements_file in __tmp0.project_details.requirements_files:
            __tmp0.log.debug("Attempting to update '{file}' contents.".format(
                file=requirements_file.path
            ))
            __tmp0._update_requirement_file(requirements_file=requirements_file)
            __tmp0.log.debug("Attempting to install requirements from '{file}'.".format(
                file=requirements_file.path
            ))
            __tmp0.from_venv(
                command="{pip} install -U -r {file}".format(
                    pip=get_pip_script_name(),
                    file=requirements_file.path
                )
            )

        __tmp0.log.debug("Validating if updated requirements did not break anything.")
        __tmp0._check()

    def _check(__tmp0) :
        """Validate if new packages did not break the project."""
        __tmp0.command(command=__tmp0.project_details.check_command)
        return True

    def _update_requirement_file(__tmp0, requirements_file) :
        """Save new requirements."""
        full_path = os.path.join(
            __tmp0.repositories_cache_path, __tmp0.repositories_cache_dir_name,
            str(__tmp0.project_details.id), requirements_file.path
        )

        # Dirty trick, to not to worry about parsing previous version
        os.remove(full_path)
        with open(full_path, "w", encoding="utf-8") as file:
            for requirement in sorted(requirements_file.requirements, key=lambda x: x.name):
                file.write("{name}{version}".format(
                    name=requirement.name,
                    version=requirement.desired_version
                ))
