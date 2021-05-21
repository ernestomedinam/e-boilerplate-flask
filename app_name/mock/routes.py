from app_name.api import rest_api, docs

from .resources.mocks import Mocks, OneMock


# mocks
rest_api.add_resource(Mocks, "/mocks")
rest_api.add_resource(OneMock, "/mocks/<int:mock_id>")
docs.register(Mocks)
docs.register(OneMock)
