from __future__ import annotations

from typing import Generic, TypeVar

from nylas.handler.handler_utils import _get_generic_type
from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource

T = TypeVar("T")


class ListableApiResource(Resource, Generic[T]):
    def list(
        self, path, headers=None, query_params=None, request_body=None
    ) -> ListResponse[T]:
        generic_type = _get_generic_type(self, ListableApiResource)
        response_json = self._http_client._execute(
            "GET", path, headers, query_params, request_body
        )

        return ListResponse.from_dict(response_json, generic_type)


class FindableApiResource(Resource, Generic[T]):
    def find(
        self, path, headers=None, query_params=None, request_body=None
    ) -> Response[T]:
        generic_type = _get_generic_type(self, FindableApiResource)
        response_json = self._http_client._execute(
            "GET", path, headers, query_params, request_body
        )

        return Response.from_dict(response_json, generic_type)


class CreatableApiResource(Resource, Generic[T]):
    def create(
        self, path, headers=None, query_params=None, request_body=None
    ) -> Response[T]:
        generic_type = _get_generic_type(self, CreatableApiResource)
        response_json = self._http_client._execute(
            "POST", path, headers, query_params, request_body
        )

        return Response.from_dict(response_json, generic_type)


class UpdatableApiResource(Resource, Generic[T]):
    def update(
        self, path, headers=None, query_params=None, request_body=None, method="PUT"
    ) -> Response[T]:
        generic_type = _get_generic_type(self, UpdatableApiResource)
        response_json = self._http_client._execute(
            method, path, headers, query_params, request_body
        )

        return Response.from_dict(response_json, generic_type)


class DestroyableApiResource(Resource, Generic[T]):
    def destroy(
        self, path, headers=None, query_params=None, request_body=None
    ) -> T | DeleteResponse:
        generic_type = _get_generic_type(self, DestroyableApiResource)
        if generic_type is None:
            generic_type = DeleteResponse

        response_json = self._http_client._execute(
            "DELETE", path, headers, query_params, request_body
        )
        return generic_type.from_dict(response_json)
