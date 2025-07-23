from typing import TypeAlias
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


class __typ2:
    """Broker class for interacting with celery_components application.

    Allows for easy sending celery_components tasks and retrieving their results.
    """

    def __init__(__tmp1, logger: Logger = None) -> None:
        """Initialize class instance."""
        __tmp1.log: Logger = logger if logger else getLogger(__name__)
        __tmp1.app: Celery = Celery("Pipwatch-api")
        configure_celery_app(celery_app=__tmp1.app)

    def get_all_active_tasks(__tmp1) -> List[ActiveTask]:
        """Return list of all currently active tasks."""
        active_tasks: List[ActiveTask] = []

        list_of_worker_tasks = __tmp1.app.control.inspect().registered().values() or []
        for worker_tasks in list_of_worker_tasks:
            active_tasks.extend(
                ActiveTask(task_object.get("name", "N/A"), task_object.get("args", "N/A"))
                for task_object in worker_tasks
            )

        return active_tasks

    def send_task(__tmp1, task_name: __typ1, args: <FILL>, kwargs: Any) :
        """Send celery_components task and receive its id."""
        __tmp1.log.info("Sending celery_components task {name} with args: {args}, kwargs: {kwargs}".format(
            name=task_name,
            args=repr(args),
            kwargs=repr(kwargs)
        ))
        return __tmp1.app.send_task(task_name, args=args, kwargs=kwargs).id

    def __tmp0(__tmp1, task_id) :
        """Check status of given celery_components task."""
        return __tmp1.app.AsyncResult(task_id)


class ProjectUpdateBroker(__typ2):
    """Encompasses logic for sending tasks for attempting project requirement update."""

    PROJECT_UPDATE_TASK_NAME = "pipwatch_worker.celery_components.tasks.process_project"

    def __init__(__tmp1, logger: Logger = None) :
        """Initialize class instance."""
        super().__init__(logger=logger)
        __tmp1.datastore = DefaultStore(
            model=Project,
            database=DATABASE
        )

    def send_update_request(__tmp1, project_id: __typ0) -> __typ1:
        """Send task for attempting update of packages for given project."""
        project: Project = __tmp1.datastore.read(document_id=project_id)  # type: ignore
        if not project:
            __tmp1.log.warning("Unable to find project with id {}, skipping sending update.".format(project_id))
            return ""

        return __tmp1.send_task(
            task_name=__tmp1.PROJECT_UPDATE_TASK_NAME,
            args=[__tmp1._get_update_request_payload(project)],
            kwargs=None
        )

    @staticmethod
    def _get_update_request_payload(project: Project) :
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
