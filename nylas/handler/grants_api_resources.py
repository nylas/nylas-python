from nylas.resources.resource import Resource


class ListableGrantsApiResource(Resource):
    def list(self, identifier: str, query_params: dict = None):
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        return self._http_client.get(path, query_params)


class FindableGrantsApiResource(Resource):
    def find(
        self,
        identifier: str,
        object_id: str,
        query_params: dict = None,
    ):
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        return self._http_client.get(path, query_params=query_params)


class CreatableGrantsApiResource(Resource):
    def create(
        self, identifier: str, request_body: dict = None, query_params: dict = None
    ):
        path = "/v3/grants/{}/{}".format(identifier, self.resource_name)
        return self._http_client.post(
            path, request_body=request_body, query_params=query_params
        )


class UpdatableGrantsApiResource(Resource):
    def update(
        self,
        identifier: str,
        object_id: str,
        request_body: dict = None,
        query_params: dict = None,
    ):
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        return self._http_client.put(
            path, request_body=request_body, query_params=query_params
        )


class DestroyableGrantsApiResource(Resource):
    def destroy(self, identifier: str, object_id: str, query_params: dict = None):
        path = "/v3/grants/{}/{}/{}".format(identifier, self.resource_name, object_id)
        return self._http_client.delete(path, query_params=query_params)
