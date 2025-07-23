from typing import TypeAlias
__typ1 : TypeAlias = "bool"
__typ0 : TypeAlias = "RequirementsFile"
"""This module contains operations related to updating requirements of project."""
from logging import Logger
import os

from pipwatch_worker.core.data_models import Project, RequirementsFile
from pipwatch_worker.core.utils import get_pip_script_name
from pipwatch_worker.worker.commands import Command, FromVirtualenv, Git
from pipwatch_worker.worker.operations.operation import Operation


class __typ2(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of attempt of updating requirements of given project."""

    def __init__(__tmp2, __tmp0: Logger, project_details: <FILL>) -> None:
        """Create method instance."""
        super().__init__(__tmp0=__tmp0, project_details=project_details)

        __tmp2.command = Command(project_id=__tmp2.project_details.id)
        __tmp2.from_venv = FromVirtualenv(project_id=__tmp2.project_details.id)
        __tmp2.git = Git(
            project_id=__tmp2.project_details.id,
            project_url=__tmp2.project_details.git_repository.url
        )

    def __tmp3(__tmp2) -> None:
        """Update requirements of given project."""
        for __tmp1 in __tmp2.project_details.requirements_files:
            __tmp2.log.debug("Attempting to update '{file}' contents.".format(
                file=__tmp1.path
            ))
            __tmp2._update_requirement_file(__tmp1=__tmp1)
            __tmp2.log.debug("Attempting to install requirements from '{file}'.".format(
                file=__tmp1.path
            ))
            __tmp2.from_venv(
                command="{pip} install -U -r {file}".format(
                    pip=get_pip_script_name(),
                    file=__tmp1.path
                )
            )

        __tmp2.log.debug("Validating if updated requirements did not break anything.")
        __tmp2._check()

    def _check(__tmp2) -> __typ1:
        """Validate if new packages did not break the project."""
        __tmp2.command(command=__tmp2.project_details.check_command)
        return True

    def _update_requirement_file(__tmp2, __tmp1: __typ0) -> None:
        """Save new requirements."""
        full_path = os.path.join(
            __tmp2.repositories_cache_path, __tmp2.repositories_cache_dir_name,
            str(__tmp2.project_details.id), __tmp1.path
        )

        # Dirty trick, to not to worry about parsing previous version
        os.remove(full_path)
        with open(full_path, "w", encoding="utf-8") as file:
            for requirement in sorted(__tmp1.requirements, key=lambda x: x.name):
                file.write("{name}{version}".format(
                    name=requirement.name,
                    version=requirement.desired_version
                ))
