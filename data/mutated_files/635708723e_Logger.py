"""This module contains operations related to creating github pull request."""
from logging import Logger
from typing import Dict, Union

import requests

from pipwatch_worker.core.data_models import Project
from pipwatch_worker.worker.operations.operation import Operation


class __typ0(Operation):  # pylint: disable=too-few-public-methods
    """Encapsulates logic of creating github pull-review."""

    DEFAULT_PR_TITLE = "[Pipwatch] - Automatic increment of requirements versions."
    DEFAULT_PR_BODY = ""

    def __init__(__tmp2, __tmp1: <FILL>, project_details) :
        """Create method instance."""
        super().__init__(__tmp1=__tmp1, project_details=project_details)

    def __tmp3(__tmp2) -> None:
        """Create github pull request."""
        raise NotImplementedError()

    def _get_pull_request_body(__tmp2) -> Dict[str, Union[bool, str]]:
        """Prepare body for PR creation call."""
        return {
            "title": __tmp2.DEFAULT_PR_TITLE,
            "head": "master",
            "base": "master",
            "body": __tmp2.DEFAULT_PR_BODY,
            "maintainer_can_modify": True
        }

    def __tmp0(__tmp2) :
        """Call github http api to create a pull request."""
        url = "{github_api_address}/repos/{owner}/{repo_name}/pulls".format(
            github_api_address=__tmp2.project_details.git_repository.github_api_address,
            owner=__tmp2.project_details.git_repository.github_project_owner,
            repo_name=__tmp2.project_details.git_repository.github_project_owner
        )
        payload = __tmp2._get_pull_request_body()
        __tmp2.log.debug("About to perform POST request to address '{url}' with payload {payload}".format(
            url=url,
            payload=str(payload)
        ))
        response = requests.post(url=url, json=payload)
        response.raise_for_status()
