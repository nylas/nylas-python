from nylas.resources.resource import Resource


class ListableAdminApiResource(Resource):
    def list(self, query_params: dict = None):
        path = "/v3/{}".format(self.resource_name)
        return self._http_client.get(path, query_params)


class FindableAdminApiResource(Resource):
    def find(
        self,
        object_id: str,
        query_params: dict = None,
    ):
        path = "/v3/{}/{}".format(self.resource_name, object_id)
        return self._http_client.get(path, query_params=query_params)


class CreatableAdminApiResource(Resource):
    def create(self, request_body: dict = None, query_params: dict = None):
        path = "/v3/{}".format(self.resource_name)
        return self._http_client.post(
            path, request_body=request_body, query_params=query_params
        )


class UpdatableAdminApiResource(Resource):
    def update(
        self,
        object_id: str,
        request_body: dict = None,
        query_params: dict = None,
    ):
        path = "/v3/{}/{}".format(self.resource_name, object_id)
        return self._http_client.put(
            path, request_body=request_body, query_params=query_params
        )


class DestroyableAdminApiResource(Resource):
    def destroy(self, object_id: str, query_params: dict = None):
        path = "/v3/{}/{}".format(self.resource_name, object_id)
        return self._http_client.delete(path, query_params=query_params)
