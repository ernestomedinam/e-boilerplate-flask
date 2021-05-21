from flask import make_response
from flask_restful import Resource, abort
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource

from ..models.mock import Mock
from ..schemas.mock import MockResponseSchema, MockPatchSchema, MockPostSchema


class Mocks(MethodResource, Resource):

    @doc(
        description="returns all mocks!",
        tags=["mocks"]
    )
    @marshal_with(MockResponseSchema(many=True), code=200)
    def get(self):
        return Mock.all()

    @doc(
        description="creates a mock!",
        tags=["mocks"]
    )
    @use_kwargs(MockPostSchema, location="json")
    @marshal_with(MockResponseSchema, code=201)
    def post(self, **kwargs):
        mock = Mock.create(**kwargs)
        if mock is None:
            abort(500)
        return mock, 201


class OneMock(MethodResource, Resource):

    @doc(
        description="returns a specific mock data!",
        tags=["mocks"]
    )
    @marshal_with(MockResponseSchema, code=200)
    def get(self, mock_id):
        mock = Mock.get(id=mock_id)
        print(f"Mock is :{mock}")
        if mock is None:
            abort(404)
        return mock, 200

    @doc(
        description="partially updates a mock!",
        tags=["mocks"]
    )
    @use_kwargs(MockPatchSchema, location="json")
    @marshal_with(MockResponseSchema, code=200)
    def patch(self, mock_id, **kwargs):
        mock = Mock.get(id=mock_id)
        if mock is None:
            abort(404)
        updated = mock.update(**kwargs)
        if not updated:
            abort(500)
        return mock, 200

    @doc(
        description="deletes a mock!",
        tags=["mocks"]
    )
    @marshal_with(None, 204)
    def delete(self, mock_id):
        mock = Mock.get(id=mock_id)
        if mock is None:
            abort(404)
        deleted = mock.delete()
        if not deleted:
            abort(500)
        return make_response({}, 204)
