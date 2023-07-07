from typing import Generic, TypeVar, get_args

from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource

T = TypeVar("T")


class ListableGrantsApiResource(Resource, Generic[T]):
    def list(self, identifier: str, query_params: dict = None) -> ListResponse[T]:
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        response_json = self._http_client.get(path, query_params)
        generic_type = get_args(self.__orig_bases__[0])[0]
        return ListResponse.from_dict(response_json, generic_type)


class FindableGrantsApiResource(Resource, Generic[T]):
    def find(
        self,
        identifier: str,
        object_id: str,
        query_params: dict = None,
    ) -> Response[T]:
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.get(path, query_params=query_params)
        generic_type = get_args(self.__orig_bases__[0])[0]
        return Response.from_dict(response_json, generic_type)


class CreatableGrantsApiResource(Resource, Generic[T]):
    def create(
        self, identifier: str, request_body: dict = None, query_params: dict = None
    ) -> Response[T]:
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        response_json = self._http_client.post(
            path, request_body=request_body, query_params=query_params
        )
        generic_type = get_args(self.__orig_bases__[0])[0]
        return Response.from_dict(response_json, generic_type)


class UpdatableGrantsApiResource(Resource, Generic[T]):
    def update(
        self,
        identifier: str,
        object_id: str,
        request_body: dict = None,
        query_params: dict = None,
    ) -> Response[T]:
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.put(
            path, request_body=request_body, query_params=query_params
        )
        generic_type = get_args(self.__orig_bases__[0])[0]
        return Response.from_dict(response_json, generic_type)


class DestroyableGrantsApiResource(Resource):
    def destroy(
        self, identifier: str, object_id: str, query_params: dict = None
    ) -> DeleteResponse:
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.delete(path, query_params=query_params)
        return DeleteResponse.from_dict(response_json)
