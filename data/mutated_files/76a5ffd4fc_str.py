from typing import TypeAlias
__typ1 : TypeAlias = "int"
"""This module contains logic for sending update-of-requirements task requests."""
from typing import Dict

from celery.result import AsyncResult
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.celery_components.broker import ProjectUpdateBroker


projects_updates_namespace = Namespace(  # pylint: disable=invalid-name
    "projects-updates",
    description="Requirements update requests for given project"
)
project_update_repr_structure = {  # pylint: disable=invalid-name
    "name": fields.String(required=True, description="Name of project update task"),
    "args": fields.String(required=True, description="Parameters used for running task")
}
project_update_repr = projects_updates_namespace.model(  # pylint: disable=invalid-name
    "ProjectUpdate", project_update_repr_structure
)


@projects_updates_namespace.route("/")
class __typ2(Resource):
    """Resource representing all ongoing update requests."""
    def __init__(__tmp2, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp2.updates_broker = ProjectUpdateBroker()

    @projects_updates_namespace.marshal_list_with(project_update_repr)
    def __tmp1(__tmp2):
        """Return list of all currently ongoing update statuses."""
        return [
            {
                "name": data.name,
                "args": data.args
            } for data in __tmp2.updates_broker.get_all_active_tasks()
        ]


@projects_updates_namespace.route("/<int:project_id>")
class __typ0(Resource):
    """Resource representing project requirements update request."""
    def __init__(__tmp2, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp2.updates_broker = ProjectUpdateBroker()

    def __tmp0(__tmp2, project_id):
        """Request update of requirements of project specified."""
        return __tmp2.updates_broker.send_update_request(project_id=project_id), 200


@projects_updates_namespace.route("/<string:task_id>")
class __typ3(Resource):
    """Resource representing requirements update task status."""
    def __init__(__tmp2, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp2.updates_broker = ProjectUpdateBroker()

    def __tmp1(__tmp2, task_id: <FILL>):
        """Return status of given update task."""
        __tmp3: AsyncResult = __tmp2.updates_broker.check_task(task_id=task_id)
        return __tmp2._async_result_to_dict(__tmp3=__tmp3), 200

    @staticmethod
    def _async_result_to_dict(__tmp3) -> Dict[str, str]:
        """Pare celery AsyncResult into human-readable representation."""
        return {
            "info": repr(__tmp3.info),
            "state": __tmp3.state,
            "taskId": __tmp3.task_id
        }
