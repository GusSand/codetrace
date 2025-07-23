from typing import TypeAlias
__typ2 : TypeAlias = "Project"
__typ0 : TypeAlias = "int"
"""This module contains broker class for streamlining interaction with celery."""
from logging import Logger, getLogger
from typing import Any, Dict, List, NamedTuple

from celery import Celery
from celery.result import AsyncResult

from pipwatch_api.core.configuration import configure_celery_app
from pipwatch_api.datastore.models import DATABASE, Project
from pipwatch_api.datastore.stores import DefaultStore


ActiveTask = NamedTuple("ActiveTask", [("name", str), ("args", str)])


class Broker:
    """Broker class for interacting with celery_components application.

    Allows for easy sending celery_components tasks and retrieving their results.
    """

    def __init__(__tmp1, logger: Logger = None) :
        """Initialize class instance."""
        __tmp1.log: Logger = logger if logger else getLogger(__name__)
        __tmp1.app: Celery = Celery("Pipwatch-api")
        configure_celery_app(celery_app=__tmp1.app)

    def get_all_active_tasks(__tmp1) :
        """Return list of all currently active tasks."""
        active_tasks: List[ActiveTask] = []

        list_of_worker_tasks = __tmp1.app.control.inspect().registered().values() or []
        for worker_tasks in list_of_worker_tasks:
            active_tasks.extend(
                ActiveTask(task_object.get("name", "N/A"), task_object.get("args", "N/A"))
                for task_object in worker_tasks
            )

        return active_tasks

    def send_task(__tmp1, task_name: <FILL>, args, __tmp2: Any) :
        """Send celery_components task and receive its id."""
        __tmp1.log.info("Sending celery_components task {name} with args: {args}, kwargs: {kwargs}".format(
            name=task_name,
            args=repr(args),
            __tmp2=repr(__tmp2)
        ))
        return __tmp1.app.send_task(task_name, args=args, __tmp2=__tmp2).id

    def check_task(__tmp1, task_id) :
        """Check status of given celery_components task."""
        return __tmp1.app.AsyncResult(task_id)


class __typ1(Broker):
    """Encompasses logic for sending tasks for attempting project requirement update."""

    PROJECT_UPDATE_TASK_NAME = "pipwatch_worker.celery_components.tasks.process_project"

    def __init__(__tmp1, logger: Logger = None) :
        """Initialize class instance."""
        super().__init__(logger=logger)
        __tmp1.datastore = DefaultStore(
            model=__typ2,
            database=DATABASE
        )

    def send_update_request(__tmp1, project_id) :
        """Send task for attempting update of packages for given project."""
        __tmp0: __typ2 = __tmp1.datastore.read(document_id=project_id)  # type: ignore
        if not __tmp0:
            __tmp1.log.warning("Unable to find project with id {}, skipping sending update.".format(project_id))
            return ""

        return __tmp1.send_task(
            task_name=__tmp1.PROJECT_UPDATE_TASK_NAME,
            args=[__tmp1._get_update_request_payload(__tmp0)],
            __tmp2=None
        )

    @staticmethod
    def _get_update_request_payload(__tmp0) :
        """Retrieve body for task request for given project."""
        return {
            "id": __tmp0.id,
            "namespace_id": __tmp0.namespace_id,
            "name": __tmp0.name,
            "git_repository": {
                "id": __tmp0.git_repository.id,
                "flavour": __tmp0.git_repository.flavour,
                "url": __tmp0.git_repository.url,
                "upstream_url": __tmp0.git_repository.upstream_url,
                "github_api_address": __tmp0.git_repository.github_api_address,
                "github_project_name": __tmp0.git_repository.github_project_name,
                "github_project_owner": __tmp0.git_repository.github_project_owner
            },
            "check_command": __tmp0.check_command,
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
                } for requirement_file in __tmp0.requirements_files
            ]
        }
