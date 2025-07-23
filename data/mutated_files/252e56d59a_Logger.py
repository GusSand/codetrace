from typing import TypeAlias
__typ1 : TypeAlias = "Project"
__typ0 : TypeAlias = "RequirementsFile"
"""This module contains operations related to updating requirements status of project in db."""
from configparser import ConfigParser  # noqa: F401 Imported for type definition
from logging import Logger

import requests

from pipwatch_worker.core.configuration import load_config_file
from pipwatch_worker.core.data_models import Project, RequirementsFile
from pipwatch_worker.worker.operations.operation import Operation


class Update(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of sending update of project requirements."""

    def __init__(__tmp0, logger: <FILL>, project_details) :
        """Create method instance."""
        super().__init__(logger=logger, project_details=project_details)
        __tmp0.config: ConfigParser = load_config_file()

    def __call__(__tmp0) :
        """Send updates for each requirement file."""
        for requirements_file in __tmp0.project_details.requirements_files:
            __tmp0.log.debug("Attempting to send updated state of requirements file '{file}'".format(
                file=requirements_file.path
            ))
            __tmp0._update_requirements_file(file=requirements_file)

    def _update_requirements_file(__tmp0, file) -> None:
        """Send update of provided requirements file."""
        url = "{api_address}/api/v1/requirements-files/{file_id}".format(
            api_address=__tmp0.config.get(section="pipwatch-api", option="address", fallback="pipwatch_api:80880"),
            file_id=str(file.id)
        )
        payload = file.to_dict()
        __tmp0.log.debug("About to perform PUT request to address '{url}' with payload {payload}".format(
            url=url,
            payload=payload
        ))
        response = requests.put(url=url, json=payload)
        response.raise_for_status()
