from typing import TypeVar, Generic, get_args

from nylas.models.delete_response import DeleteResponse
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource

T = TypeVar("T")


class ListableAdminApiResource(Resource, Generic[T]):
    def list(self, query_params: dict = None) -> ListResponse:
        path = "/v3/{}".format(self.resource_name)
        response_json = self._http_client.get(path, query_params)
        generic_type = get_args(self.__orig_bases__[0])[0]
        return ListResponse.from_dict(response_json, generic_type)


class FindableAdminApiResource(Resource, Generic[T]):
    def find(
        self,
        object_id: str,
        query_params: dict = None,
    ) -> Response:
        path = "/v3/{}/{}".format(self.resource_name, object_id)
        response_json = self._http_client.get(path, query_params=query_params)
        generic_type = get_args(self.__orig_bases__[0])[0]
        return Response.from_dict(response_json, generic_type)


class CreatableAdminApiResource(Resource, Generic[T]):
    def create(self, request_body: dict = None, query_params: dict = None) -> Response:
        path = "/v3/{}".format(self.resource_name)
        response_json = self._http_client.post(
            path, request_body=request_body, query_params=query_params
        )
        generic_type = get_args(self.__orig_bases__[0])[0]
        return Response.from_dict(response_json, generic_type)


class UpdatableAdminApiResource(Resource, Generic[T]):
    def update(
        self,
        object_id: str,
        request_body: dict = None,
        query_params: dict = None,
    ) -> Response:
        path = "/v3/{}/{}".format(self.resource_name, object_id)
        response_json = self._http_client.put(
            path, request_body=request_body, query_params=query_params
        )
        generic_type = get_args(self.__orig_bases__[0])[0]
        return Response.from_dict(response_json, generic_type)


class DestroyableAdminApiResource(Resource):
    def destroy(self, object_id: str, query_params: dict = None) -> DeleteResponse:
        path = "/v3/{}/{}".format(self.resource_name, object_id)
        response_json = self._http_client.delete(path, query_params=query_params)
        return DeleteResponse.from_dict(response_json)
