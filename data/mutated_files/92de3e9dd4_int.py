from typing import TypeAlias
__typ1 : TypeAlias = "Project"
"""This module contains logic for handling operations on project-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE, Project as ProjectModel, RequirementsFile, Tag
from pipwatch_api.datastore.stores import NestedDocument, WithNestedDocumentsStore

from pipwatch_api.namespaces.v1.git_repository import git_repository_repr_structure
from pipwatch_api.namespaces.v1.requirements_files import requirements_file_simple_repr_structure
from pipwatch_api.namespaces.v1.tags import tag_representation_structure


TagNestedDocument = NestedDocument("tags", Tag, "name")  # pylint: disable=invalid-name
RequirementsFilesNestedDocument = NestedDocument(  # pylint: disable=invalid-name
    "requirements_files",
    RequirementsFile,
    "id")

projects_namespace = Namespace(  # pylint: disable=invalid-name
    "projects",
    description="CRUD operations on projects"
)
git_repository_repr = projects_namespace.model(  # pylint: disable=invalid-name
    "GitRepository",
    git_repository_repr_structure
)
tag_representation = projects_namespace.model(  # pylint: disable=invalid-name
    "Tag",
    tag_representation_structure
)
project_representation_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description="If of given project, unique across the database"),
    "name": fields.String(required=True, description="Name of project (i.e. 'pipwatch')"),
    "git_repository": fields.Nested(git_repository_repr),
    "check_command": fields.String(description="Command to be used to verify update success (i.e. 'test')"),
    "namespace_id": fields.Integer(attribute="namespace.id"),
    "namespace": fields.String(attribute="namespace.name"),
    "tags": fields.List(fields.Nested(tag_representation))
}
project_representation = projects_namespace.model(  # pylint: disable=invalid-name
    "Project",
    project_representation_structure
)
requirements_file_simple_repr = projects_namespace.model(  # pylint: disable=invalid-name
    "RequirementsFile",
    requirements_file_simple_repr_structure
)
project_repr_req_files = projects_namespace.inherit(  # pylint: disable=invalid-name
    "Project with requirements files",
    project_representation,
    {"requirements_files": fields.List(fields.Nested(requirements_file_simple_repr))}
)


@projects_namespace.route("/")
class __typ0(Resource):
    """Resource representing projects collection."""
    def __init__(__tmp1, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp1.datastore = WithNestedDocumentsStore(
            model=ProjectModel,
            database=DATABASE,
            nested_documents_specs=[TagNestedDocument, RequirementsFilesNestedDocument]
        )

    @projects_namespace.marshal_list_with(project_representation)
    def get(__tmp1):
        """Return list of all projects."""
        return __tmp1.datastore.read_all()

    @projects_namespace.doc("create_project")
    @projects_namespace.expect(project_repr_req_files)
    @projects_namespace.marshal_with(project_repr_req_files, code=201)
    def post(__tmp1):
        """Create a new project."""
        if not request.json:
            return None, 400

        created_document: ProjectModel = __tmp1.datastore.create(document=request.json)
        return created_document, 201


@projects_namespace.route("/<int:project_id>")
@projects_namespace.response(404, "Project not found.")
class __typ1(Resource):
    """Resource representing operations on single project."""
    def __init__(__tmp1, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp1.datastore = WithNestedDocumentsStore(
            model=ProjectModel,
            database=DATABASE,
            nested_documents_specs=[TagNestedDocument, RequirementsFilesNestedDocument]
        )

    @projects_namespace.marshal_with(project_repr_req_files)
    @projects_namespace.response(200, "Namespace found.")
    def get(__tmp1, __tmp0: <FILL>):
        """Return project with given id."""
        document: ProjectModel = __tmp1.datastore.read(document_id=__tmp0)
        if not document:
            return None, 404

        return document, 200

    @projects_namespace.expect(project_repr_req_files)
    @projects_namespace.marshal_with(project_repr_req_files, code=200)
    @projects_namespace.response(400, "Invalid request.")
    def put(__tmp1, __tmp0: int):
        """Update project with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: ProjectModel = __tmp1.datastore.update(document_id=__tmp0, document=received_document)
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(__tmp1, __tmp0):
        """Delete project with given id."""
        __tmp1.datastore.delete(document_id=__tmp0)
        return None, 204
