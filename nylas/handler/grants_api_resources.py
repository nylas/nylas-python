from nylas.model.delete_response import DeleteResponse
from nylas.model.list_response import ListResponse
from nylas.model.response import Response
from nylas.resources.resource import Resource


class ListableGrantsApiResource(Resource):
    def list(self, identifier: str, query_params: dict = None) -> ListResponse:
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        response_json = self._http_client.get(path, query_params)
        return ListResponse.from_dict(response_json)


class FindableGrantsApiResource(Resource):
    def find(
        self,
        identifier: str,
        object_id: str,
        query_params: dict = None,
    ) -> Response:
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.get(path, query_params=query_params)
        return Response.from_dict(response_json)


class CreatableGrantsApiResource(Resource):
    def create(
        self, identifier: str, request_body: dict = None, query_params: dict = None
    ) -> Response:
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        response_json = self._http_client.post(
            path, request_body=request_body, query_params=query_params
        )
        return Response.from_dict(response_json)


class UpdatableGrantsApiResource(Resource):
    def update(
        self,
        identifier: str,
        object_id: str,
        request_body: dict = None,
        query_params: dict = None,
    ) -> Response:
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.put(
            path, request_body=request_body, query_params=query_params
        )
        return Response.from_dict(response_json)


class DestroyableGrantsApiResource(Resource):
    def destroy(
        self, identifier: str, object_id: str, query_params: dict = None
    ) -> DeleteResponse:
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        response_json = self._http_client.delete(path, query_params=query_params)
        return DeleteResponse.from_dict(response_json)
