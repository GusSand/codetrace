from typing import TypeAlias
__typ1 : TypeAlias = "Project"
__typ0 : TypeAlias = "RequirementsFile"
"""This module contains operations related to parsing requirements of project."""
from logging import Logger
import os
from typing import Any

import requirements

from pipwatch_worker.core.data_models import Project, RequirementsFile, Requirement
from pipwatch_worker.worker.operations.operation import Operation


class Parse(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of parsing requirements of given project (and keeping them up to date)."""

    def __init__(__tmp2, logger: Logger, project_details: __typ1) :
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)

    def __tmp0(__tmp2) -> None:
        """Parse requirements of given project."""
        for __tmp1 in __tmp2.project_details.requirements_files:
            __tmp2.log.debug("Attempting to parse requirements file '{file}'".format(
                __tmp3=__tmp1.path
            ))
            __tmp2._parse_requirements_file(__tmp1=__tmp1)

    def _parse_requirements_file(__tmp2, __tmp1: __typ0) -> None:
        """Parse all packages required by given file."""
        full_path = os.path.join(
            __tmp2.repositories_cache_path, __tmp2.repositories_cache_dir_name,
            str(__tmp2.project_details.id), __tmp1.path
        )

        __tmp2.log.debug("Attempting to open file '{file}'".format(__tmp3=full_path))
        with open(full_path, "r", encoding="utf-8") as __tmp3:
            for requirement_raw in requirements.parse(__tmp3):
                __tmp2.log.debug("Parsing read requirement of {package}".format(
                    package=repr(requirement_raw)
                ))
                __tmp2._parse_requirement(__tmp3=__tmp1, requirement=requirement_raw)

    def _parse_requirement(__tmp2, __tmp3: __typ0, requirement: <FILL>) -> None:
        """Parse single requirement of given file."""
        previous_entry = next((x for x in __tmp3.requirements if x.name == requirement.name), None)
        package_version_from_project = str(requirement.specs) if requirement.specs else ""

        if not previous_entry:
            __tmp2.log.debug("Previous requirement entry not found. Adding it.")
            __tmp3.requirements.append(Requirement(
                name=requirement.name,
                current_version=package_version_from_project
            ))

        if previous_entry and (previous_entry.current_version != package_version_from_project):
            __tmp2.log.debug("Overriding {package} version of {prev_version} with {version}".format(
                package=previous_entry.name,
                prev_version=previous_entry.current_version,
                version=package_version_from_project
            ))
            previous_entry.current_version = package_version_from_project
