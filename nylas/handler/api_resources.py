from __future__ import annotations

from nylas.models.response import Response, ListResponse, DeleteResponse
from nylas.resources.resource import Resource

# pylint: disable=too-few-public-methods,missing-class-docstring,missing-function-docstring


class ListableApiResource(Resource):
    def list(
        self,
        path,
        response_type,
        headers=None,
        query_params=None,
        request_body=None,
        overrides=None,
    ) -> ListResponse:
        response_json, response_headers = self._http_client._execute(
            "GET", path, headers, query_params, request_body, overrides=overrides
        )

        return ListResponse.from_dict(response_json, response_type, response_headers)


class FindableApiResource(Resource):
    def find(
        self,
        path,
        response_type,
        headers=None,
        query_params=None,
        request_body=None,
        overrides=None,
    ) -> Response:
        response_json, response_headers = self._http_client._execute(
            "GET", path, headers, query_params, request_body, overrides=overrides
        )

        return Response.from_dict(response_json, response_type, response_headers)


class CreatableApiResource(Resource):
    def create(
        self,
        path,
        response_type,
        headers=None,
        query_params=None,
        request_body=None,
        overrides=None,
    ) -> Response:

        response_json, response_headers = self._http_client._execute(
            "POST", path, headers, query_params, request_body, overrides=overrides
        )

        return Response.from_dict(response_json, response_type, response_headers)


class UpdatableApiResource(Resource):
    def update(
        self,
        path,
        response_type,
        headers=None,
        query_params=None,
        request_body=None,
        method="PUT",
        overrides=None,
    ):
        response_json, response_headers = self._http_client._execute(
            method, path, headers, query_params, request_body, overrides=overrides
        )

        return Response.from_dict(response_json, response_type, response_headers)


class UpdatablePatchApiResource(Resource):
    def patch(
        self,
        path,
        response_type,
        headers=None,
        query_params=None,
        request_body=None,
        method="PATCH",
        overrides=None,
    ):
        response_json, response_headers = self._http_client._execute(
            method, path, headers, query_params, request_body, overrides=overrides
        )

        return Response.from_dict(response_json, response_type, response_headers)


class DestroyableApiResource(Resource):
    def destroy(
        self,
        path,
        response_type=None,
        headers=None,
        query_params=None,
        request_body=None,
        overrides=None,
    ):
        if response_type is None:
            response_type = DeleteResponse

        response_json, response_headers = self._http_client._execute(
            "DELETE", path, headers, query_params, request_body, overrides=overrides
        )

        # Check if the response type is a dataclass_json class
        if hasattr(response_type, "from_dict") and not hasattr(response_type, "headers"):
            return response_type.from_dict(response_json)
        return response_type.from_dict(response_json, headers=response_headers)
