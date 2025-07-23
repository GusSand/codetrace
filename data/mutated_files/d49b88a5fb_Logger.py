from typing import TypeAlias
__typ3 : TypeAlias = "Project"
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "RequirementsFile"
"""This module contains operations related to parsing requirements of project."""
from logging import Logger
import os
from typing import Any

import requirements

from pipwatch_worker.core.data_models import Project, RequirementsFile, Requirement
from pipwatch_worker.worker.operations.operation import Operation


class __typ1(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of parsing requirements of given project (and keeping them up to date)."""

    def __init__(__tmp0, logger: <FILL>, project_details) :
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)

    def __call__(__tmp0) :
        """Parse requirements of given project."""
        for requirements_file in __tmp0.project_details.requirements_files:
            __tmp0.log.debug("Attempting to parse requirements file '{file}'".format(
                file=requirements_file.path
            ))
            __tmp0._parse_requirements_file(requirements_file=requirements_file)

    def _parse_requirements_file(__tmp0, requirements_file) :
        """Parse all packages required by given file."""
        full_path = os.path.join(
            __tmp0.repositories_cache_path, __tmp0.repositories_cache_dir_name,
            str(__tmp0.project_details.id), requirements_file.path
        )

        __tmp0.log.debug("Attempting to open file '{file}'".format(file=full_path))
        with open(full_path, "r", encoding="utf-8") as file:
            for requirement_raw in requirements.parse(file):
                __tmp0.log.debug("Parsing read requirement of {package}".format(
                    package=repr(requirement_raw)
                ))
                __tmp0._parse_requirement(file=requirements_file, requirement=requirement_raw)

    def _parse_requirement(__tmp0, file, requirement) :
        """Parse single requirement of given file."""
        previous_entry = next((x for x in file.requirements if x.name == requirement.name), None)
        package_version_from_project = str(requirement.specs) if requirement.specs else ""

        if not previous_entry:
            __tmp0.log.debug("Previous requirement entry not found. Adding it.")
            file.requirements.append(Requirement(
                name=requirement.name,
                current_version=package_version_from_project
            ))

        if previous_entry and (previous_entry.current_version != package_version_from_project):
            __tmp0.log.debug("Overriding {package} version of {prev_version} with {version}".format(
                package=previous_entry.name,
                prev_version=previous_entry.current_version,
                version=package_version_from_project
            ))
            previous_entry.current_version = package_version_from_project
