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

    def __init__(__tmp2, logger: Logger = None) :
        """Initialize class instance."""
        __tmp2.log: Logger = logger if logger else getLogger(__name__)
        __tmp2.app: Celery = Celery("Pipwatch-api")
        configure_celery_app(celery_app=__tmp2.app)

    def __tmp0(__tmp2) -> List[ActiveTask]:
        """Return list of all currently active tasks."""
        active_tasks: List[ActiveTask] = []

        list_of_worker_tasks = __tmp2.app.control.inspect().registered().values() or []
        for worker_tasks in list_of_worker_tasks:
            active_tasks.extend(
                ActiveTask(task_object.get("name", "N/A"), task_object.get("args", "N/A"))
                for task_object in worker_tasks
            )

        return active_tasks

    def send_task(__tmp2, task_name, args, kwargs) :
        """Send celery_components task and receive its id."""
        __tmp2.log.info("Sending celery_components task {name} with args: {args}, kwargs: {kwargs}".format(
            name=task_name,
            args=repr(args),
            kwargs=repr(kwargs)
        ))
        return __tmp2.app.send_task(task_name, args=args, kwargs=kwargs).id

    def check_task(__tmp2, task_id: <FILL>) :
        """Check status of given celery_components task."""
        return __tmp2.app.AsyncResult(task_id)


class ProjectUpdateBroker(Broker):
    """Encompasses logic for sending tasks for attempting project requirement update."""

    PROJECT_UPDATE_TASK_NAME = "pipwatch_worker.celery_components.tasks.process_project"

    def __init__(__tmp2, logger: Logger = None) :
        """Initialize class instance."""
        super().__init__(logger=logger)
        __tmp2.datastore = DefaultStore(
            model=Project,
            database=DATABASE
        )

    def __tmp3(__tmp2, project_id) :
        """Send task for attempting update of packages for given project."""
        __tmp1: Project = __tmp2.datastore.read(document_id=project_id)  # type: ignore
        if not __tmp1:
            __tmp2.log.warning("Unable to find project with id {}, skipping sending update.".format(project_id))
            return ""

        return __tmp2.send_task(
            task_name=__tmp2.PROJECT_UPDATE_TASK_NAME,
            args=[__tmp2._get_update_request_payload(__tmp1)],
            kwargs=None
        )

    @staticmethod
    def _get_update_request_payload(__tmp1) :
        """Retrieve body for task request for given project."""
        return {
            "id": __tmp1.id,
            "namespace_id": __tmp1.namespace_id,
            "name": __tmp1.name,
            "git_repository": {
                "id": __tmp1.git_repository.id,
                "flavour": __tmp1.git_repository.flavour,
                "url": __tmp1.git_repository.url,
                "upstream_url": __tmp1.git_repository.upstream_url,
                "github_api_address": __tmp1.git_repository.github_api_address,
                "github_project_name": __tmp1.git_repository.github_project_name,
                "github_project_owner": __tmp1.git_repository.github_project_owner
            },
            "check_command": __tmp1.check_command,
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
                } for requirement_file in __tmp1.requirements_files
            ]
        }
