from typing import TypeAlias
__typ0 : TypeAlias = "Namespace"
"""This module contains logic for handling operations on namespace-related requests."""

from typing import Dict  # noqa: F401 Imported for type definition

from flask import request
from flask_restplus import fields, Namespace as FlaskNamespace, Resource

from pipwatch_api.datastore.models import DATABASE, Namespace as NamespaceModel
from pipwatch_api.datastore.stores import DefaultStore

from pipwatch_api.namespaces.v1.projects import project_representation_structure


namespaces_namespace = FlaskNamespace(  # pylint: disable=invalid-name
    "namespaces",
    description="CRUD operations on projects namespaces"
)
project_repr = namespaces_namespace.model(  # pylint: disable=invalid-name
    "Project",
    project_representation_structure
)
namespace_repr_structure = {  # pylint: disable=invalid-name
    "id": fields.Integer(readOnly=True, description="Id of given namespace, unique across the database"),
    "name": fields.String(required=True, description="Name of namespace (i.e. 'building-tools')")
}
namespace_repr = namespaces_namespace.model("Namespace", namespace_repr_structure)  # pylint: disable=invalid-name
namespace_repr_detailed = namespaces_namespace.inherit(  # pylint: disable=invalid-name
    "Namespace with projects",
    namespace_repr, {"projects": fields.List(fields.Nested(project_repr))}
)


@namespaces_namespace.route("/")
class __typ1(Resource):
    """Resource representing namespaces collection."""
    def __init__(__tmp0, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp0.datastore = DefaultStore(model=NamespaceModel, database=DATABASE)

    @namespaces_namespace.marshal_list_with(namespace_repr)
    def get(__tmp0):
        """Return list of all namespaces."""
        return __tmp0.datastore.read_all()

    @namespaces_namespace.doc("create_namespace")
    @namespaces_namespace.expect(namespace_repr)
    @namespaces_namespace.marshal_with(namespace_repr, code=201)
    def post(__tmp0):
        """Create a new namespace."""
        if not request.json:
            return None, 400

        created_document: NamespaceModel = __tmp0.datastore.create(document=request.json)
        return created_document, 201


@namespaces_namespace.route("/<int:namespace_id>")
@namespaces_namespace.response(404, "Namespace not found.")
class __typ0(Resource):
    """Resource representing operations on single namespace."""
    def __init__(__tmp0, *args, **kwargs):
        """Initialize resource instance."""
        super().__init__(*args, **kwargs)
        __tmp0.datastore = DefaultStore(model=NamespaceModel, database=DATABASE)

    @namespaces_namespace.marshal_with(namespace_repr_detailed)
    @namespaces_namespace.response(200, "Namespace found.")
    def get(__tmp0, namespace_id: <FILL>):
        """Return namespace with given id."""
        document: NamespaceModel = __tmp0.datastore.read(document_id=namespace_id)
        if not document:
            return None, 404

        return document, 200

    @namespaces_namespace.expect(namespace_repr)
    @namespaces_namespace.marshal_with(namespace_repr, code=200)
    @namespaces_namespace.response(400, "Invalid request.")
    def put(__tmp0, namespace_id: int):
        """Update namespace with given id."""
        if not request.json:
            return None, 400

        received_document: Dict = request.json
        updated_document: NamespaceModel = __tmp0.datastore.update(document_id=namespace_id, document=received_document)
        if not updated_document:
            return None, 404

        return updated_document, 200

    def delete(__tmp0, namespace_id):
        """Delete namespace with given id."""
        __tmp0.datastore.delete(document_id=namespace_id)
        return None, 204
