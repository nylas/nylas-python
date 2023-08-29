from __future__ import annotations

from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource


class ListableApiResource(Resource):
    def list(
        self, path, response_type, headers=None, query_params=None, request_body=None
    ) -> ListResponse:
        response_json = self._http_client._execute(
            "GET", path, headers, query_params, request_body
        )

        return ListResponse.from_dict(response_json, response_type)


class FindableApiResource(Resource):
    def find(
        self, path, response_type, headers=None, query_params=None, request_body=None
    ) -> Response:
        response_json = self._http_client._execute(
            "GET", path, headers, query_params, request_body
        )

        return Response.from_dict(response_json, response_type)


class CreatableApiResource(Resource):
    def create(
        self, path, response_type, headers=None, query_params=None, request_body=None
    ) -> Response:
        response_json = self._http_client._execute(
            "POST", path, headers, query_params, request_body
        )

        return Response.from_dict(response_json, response_type)


class UpdatableApiResource(Resource):
    def update(
        self,
        path,
        response_type,
        headers=None,
        query_params=None,
        request_body=None,
        method="PUT",
    ):
        response_json = self._http_client._execute(
            method, path, headers, query_params, request_body
        )

        return Response.from_dict(response_json, response_type)


class DestroyableApiResource(Resource):
    def destroy(
        self,
        path,
        response_type=None,
        headers=None,
        query_params=None,
        request_body=None,
    ):
        if response_type is None:
            response_type = DeleteResponse

        response_json = self._http_client._execute(
            "DELETE", path, headers, query_params, request_body
        )
        return Response.from_dict(response_json, response_type)