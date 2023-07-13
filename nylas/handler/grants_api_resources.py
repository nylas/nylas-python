from __future__ import annotations

from typing import Generic, TypeVar, get_args

from nylas.handler.handler_utils import _get_generic_type
from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource

T = TypeVar("T")


class ListableGrantsApiResource(Resource, Generic[T]):
    def list(self, identifier: str, query_params: dict = None) -> ListResponse[T]:
        generic_type = _get_generic_type(self, ListableGrantsApiResource)
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        response_json = self._http_client.get(path, query_params)
        return ListResponse.from_dict(response_json, generic_type)


class FindableGrantsApiResource(Resource, Generic[T]):
    def find(
        self,
        identifier: str,
        object_id: str,
        query_params: dict = None,
    ) -> Response[T]:
        generic_type = _get_generic_type(self, FindableGrantsApiResource)
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.get(path, query_params=query_params)
        return Response.from_dict(response_json, generic_type)


class CreatableGrantsApiResource(Resource, Generic[T]):
    def create(
        self, identifier: str, request_body: dict = None, query_params: dict = None
    ) -> Response[T]:
        generic_type = _get_generic_type(self, CreatableGrantsApiResource)
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        response_json = self._http_client.post(
            path, request_body=request_body, query_params=query_params
        )
        return Response.from_dict(response_json, generic_type)


class UpdatableGrantsApiResource(Resource, Generic[T]):
    def update(
        self,
        identifier: str,
        object_id: str,
        request_body: dict = None,
        query_params: dict = None,
    ) -> Response[T]:
        generic_type = _get_generic_type(self, UpdatableGrantsApiResource)
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.put(
            path, request_body=request_body, query_params=query_params
        )
        return Response.from_dict(response_json, generic_type)


class DestroyableGrantsApiResource(Resource, Generic[T]):
    def destroy(
        self, identifier: str, object_id: str, query_params: dict = None
    ) -> T | DeleteResponse:
        generic_type = _get_generic_type(self, DestroyableGrantsApiResource)
        if generic_type is None:
            generic_type = DeleteResponse

        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.delete(path, query_params=query_params)
        return generic_type.from_dict(response_json)
