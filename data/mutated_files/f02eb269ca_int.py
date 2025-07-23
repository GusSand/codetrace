from typing import TypeAlias
__typ0 : TypeAlias = "GitRepository"
"""This module contains logic for handling operations on git-repository-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import Namespace, Resource, fields

from pipwatch_api.datastore.models import DATABASE, GitRepository as GitRepositoryModel
from pipwatch_api.datastore.stores import DefaultStore

git_repositories_namespace = Namespace(  # pylint: disable=invalid-name
    "git-repositories",
    description="CRUD operations on git repositories"
)
git_repository_repr_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description="Id of given git repository, unique across database"),
    "flavour": fields.String(required=True, description="Type of git repository (git|github|gerrit)"),
    "url": fields.String(required=True, description="Git url for repository to use while cloning"),
    "upstream_url": fields.String(required=False, description="[Github only] Link to upstream repository"),
    "github_api_address": fields.String(required=False, description="[Github only] Link to github instance"),
    "github_project_name": fields.String(required=False, description="[Github only] Name of upstream project"),
    "github_project_owner": fields.String(required=False, description="[Github only] Owner of upstream project")
}
git_repository_repr = git_repositories_namespace.model(  # pylint: disable=invalid-name
    "GitRepository", git_repository_repr_structure
)


@git_repositories_namespace.route("/")
class __typ1(Resource):
    """Resource representing git repositories collection."""
    def __init__(__tmp2, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp2.datastore = DefaultStore(model=GitRepositoryModel, database=DATABASE)

    @git_repositories_namespace.marshal_list_with(git_repository_repr)
    def __tmp1(__tmp2):
        """Return list of all git repositories."""
        return __tmp2.datastore.read_all()

    @git_repositories_namespace.doc("create_git_repository")
    @git_repositories_namespace.expect(git_repository_repr)
    @git_repositories_namespace.marshal_with(git_repository_repr, code=201)
    def __tmp0(__tmp2):
        """Create a new git repository."""
        if not request.json:
            return None, 400

        created_git_repository: GitRepositoryModel = __tmp2.datastore.create(document=request.json)
        return created_git_repository, 201


@git_repositories_namespace.route("/<int:git_repo_id>")
@git_repositories_namespace.response(404, "Git repository not found.")
class __typ0(Resource):
    """Resource representing operations on single git repository."""
    def __init__(__tmp2, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp2.datastore = DefaultStore(model=GitRepositoryModel, database=DATABASE)

    @git_repositories_namespace.marshal_with(git_repository_repr)
    @git_repositories_namespace.response(200, "Git repository found.")
    def __tmp1(__tmp2, __tmp3: <FILL>):
        """Return git repository with given id."""
        document: GitRepositoryModel = __tmp2.datastore.read(document_id=__tmp3)
        if not document:
            return None, 404

        return document, 200

    @git_repositories_namespace.expect(git_repository_repr)
    @git_repositories_namespace.marshal_with(git_repository_repr, code=200)
    @git_repositories_namespace.response(400, "Invalid request.")
    def put(__tmp2, __tmp3):
        """Update git repository with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: GitRepositoryModel = __tmp2.datastore.update(
            document_id=__tmp3, document=received_document
        )

        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(__tmp2, __tmp3):
        """Delete git repository with given id."""
        __tmp2.datastore.delete(document_id=__tmp3)
        return None, 204
