from typing import TypeAlias
__typ4 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
"""This module contains broker class for streamlining interaction with celery."""
from logging import Logger, getLogger
from typing import Any, Dict, List, NamedTuple

from celery import Celery
from celery.result import AsyncResult

from pipwatch_api.core.configuration import configure_celery_app
from pipwatch_api.datastore.models import DATABASE, Project
from pipwatch_api.datastore.stores import DefaultStore


ActiveTask = NamedTuple("ActiveTask", [("name", __typ1), ("args", __typ1)])


class __typ3:
    """Broker class for interacting with celery_components application.

    Allows for easy sending celery_components tasks and retrieving their results.
    """

    def __init__(__tmp3, logger: Logger = None) -> None:
        """Initialize class instance."""
        __tmp3.log: Logger = logger if logger else getLogger(__name__)
        __tmp3.app: Celery = Celery("Pipwatch-api")
        configure_celery_app(celery_app=__tmp3.app)

    def __tmp5(__tmp3) -> List[ActiveTask]:
        """Return list of all currently active tasks."""
        active_tasks: List[ActiveTask] = []

        list_of_worker_tasks = __tmp3.app.control.inspect().registered().values() or []
        for worker_tasks in list_of_worker_tasks:
            active_tasks.extend(
                ActiveTask(task_object.get("name", "N/A"), task_object.get("args", "N/A"))
                for task_object in worker_tasks
            )

        return active_tasks

    def send_task(__tmp3, __tmp8: __typ1, __tmp2: __typ4, __tmp4: __typ4) -> __typ1:
        """Send celery_components task and receive its id."""
        __tmp3.log.info("Sending celery_components task {name} with args: {args}, kwargs: {kwargs}".format(
            name=__tmp8,
            __tmp2=repr(__tmp2),
            __tmp4=repr(__tmp4)
        ))
        return __tmp3.app.send_task(__tmp8, __tmp2=__tmp2, __tmp4=__tmp4).id

    def __tmp1(__tmp3, __tmp0) -> AsyncResult:
        """Check status of given celery_components task."""
        return __tmp3.app.AsyncResult(__tmp0)


class __typ2(__typ3):
    """Encompasses logic for sending tasks for attempting project requirement update."""

    PROJECT_UPDATE_TASK_NAME = "pipwatch_worker.celery_components.tasks.process_project"

    def __init__(__tmp3, logger: Logger = None) -> None:
        """Initialize class instance."""
        super().__init__(logger=logger)
        __tmp3.datastore = DefaultStore(
            model=Project,
            database=DATABASE
        )

    def __tmp6(__tmp3, __tmp7: __typ0) -> __typ1:
        """Send task for attempting update of packages for given project."""
        project: Project = __tmp3.datastore.read(document_id=__tmp7)  # type: ignore
        if not project:
            __tmp3.log.warning("Unable to find project with id {}, skipping sending update.".format(__tmp7))
            return ""

        return __tmp3.send_task(
            __tmp8=__tmp3.PROJECT_UPDATE_TASK_NAME,
            __tmp2=[__tmp3._get_update_request_payload(project)],
            __tmp4=None
        )

    @staticmethod
    def _get_update_request_payload(project: <FILL>) -> Dict[__typ1, __typ4]:
        """Retrieve body for task request for given project."""
        return {
            "id": project.id,
            "namespace_id": project.namespace_id,
            "name": project.name,
            "git_repository": {
                "id": project.git_repository.id,
                "flavour": project.git_repository.flavour,
                "url": project.git_repository.url,
                "upstream_url": project.git_repository.upstream_url,
                "github_api_address": project.git_repository.github_api_address,
                "github_project_name": project.git_repository.github_project_name,
                "github_project_owner": project.git_repository.github_project_owner
            },
            "check_command": project.check_command,
            "requirements_files": [
                {
                    "id": requirement_file.id,
                    "path": requirement_file.path,
                    "status": requirement_file.status,
                    "requirements": [
                        {
                            "id": requirement.id,
                            "name": requirement.name,
                            "current_version": requirement.current_version,
                            "desired_version": requirement.desired_version,
                            "status": requirement.status,
                        } for requirement in requirement_file.requirements
                    ]
                } for requirement_file in project.requirements_files
            ]
        }
