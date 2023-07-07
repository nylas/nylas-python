from nylas.handler.http_client import HttpClient
from nylas.models.list_response import ListResponse
from nylas.models.response import Response
from nylas.resources.resource import Resource


class Providers(Resource):
    def __init__(self, http_client: HttpClient, client_id: str):
        super(Providers, self).__init__("providers", http_client)
        self.client_id = client_id

    def list(self) -> ListResponse:
        """
        List all providers.

        Returns:
            ListResponse: The list of providers.
        """

        json_response = self._http_client.get(
            "/v3/connect/providers/find", query_params={"client_id": self.client_id}
        )
        return ListResponse.from_dict(json_response)

    def detect(self, query_params: dict) -> Response:
        """
        Detect providers.

        Args:
            query_params (dict): The query parameters to send to the API.

        Returns:
            Response: The detected provider.
        """

        json_response = self._http_client.get(
            "/v3/connect/providers/detect",
            query_params={"client_id": self.client_id, **query_params},
        )
        return Response.from_dict(json_response)
